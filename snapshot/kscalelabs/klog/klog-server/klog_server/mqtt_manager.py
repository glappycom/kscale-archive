import paho.mqtt.client as mqtt
import logging
import json
import sys
from .state import GlobalState, KlogDeviceType, KlogDeviceStatus, CollectionState, SyncState
import colorlogging

logger = logging.getLogger(__name__)
# Set up logger for this module
logger = logging.getLogger(__name__)
colorlogging.configure(
    logger=logger,
    remove_existing_handlers=True,
    hide_if_not_interactive=False,
    level=logging.DEBUG,
)

class MqttManager:
    def __init__(self, state: GlobalState, client_id: str):
        self.client = mqtt.Client(client_id=client_id)
        self.state = state
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def start(self, host: str, port: int, keepalive: int = 60):
        self.client.connect(host, port, keepalive)
        self.client.loop_forever()

    def scan(self):
        logger.debug("Sending re-registration request.")
        self.publish("device/scan", json.dumps({}))

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to MQTT broker.")
            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
            client.subscribe("#", 1) # Subscribe to all topics for debugging
        else:
            logger.error(f"Failed to connect to MQTT broker, return code {rc}")
            sys.exit(1)

    def _on_message(self, client, userdata, msg: mqtt.MQTTMessage):
        logger.info("Received message on %s: %s", msg.topic, msg.payload.decode())
        try:
            msg_json = json.loads(msg.payload.decode())
        except json.JSONDecodeError:
            logger.error("Failed to decode JSON from message: %s", msg.payload.decode())
            return

        if msg.topic == "logging/run/start":
            self.state.start_run(robot=msg_json.get("robot"), run_id=msg_json.get("run_id"))

        elif msg.topic == "logging/run/stop":
            self.state.stop_run(run_id=msg_json.get("run_id"))

        elif msg.topic.startswith("device/register/"):
            try:
                dev_type = KlogDeviceType(msg_json.get("type"))
            except ValueError:
                logger.error(f"Invalid device type: {msg_json.get('type')}")
                return
            self.state.register_device(dev_id=msg_json.get("device"), dev_type=dev_type, description=msg_json.get("description"))

        elif msg.topic.startswith("device/status"):
            try:
                status = KlogDeviceStatus(msg_json.get("status"))
            except ValueError:
                logger.error(f"Invalid device status: {msg_json.get('status')}")
                return
            self.state.update_status(dev_id=msg_json.get("device"), status=status, disconnect_type=msg_json.get("disconnect_type"))

        elif msg.topic.startswith("logging/collection_state/"):
            try:
                collection_state = CollectionState(msg_json.get("collection_state"))
            except ValueError:
                logger.error(f"Invalid collection state: {msg_json.get('collection_state')}")
                return
            self.state.update_collection_state(
                dev_id=msg_json.get("device"),
                state=collection_state,
                run_id=msg_json.get("run_id"),
                failure_type=msg_json.get("failure_type")
            )

        elif msg.topic.startswith("logging/sync_state/"):
            try:
                sync_state = SyncState(msg_json.get("sync_state"))
            except ValueError:
                logger.error(f"Invalid sync state: {msg_json.get('sync_state')}")
                return
            self.state.update_sync_state(
                dev_id=msg_json.get("device"),
                state=sync_state,
                run_id=msg_json.get("run_id"),
                failure_type=msg_json.get("failure_type")
            )

        logger.debug("Active runs:\n  %s", "\n  ".join([f"{run.run_id}: {run.state.name}" for run in self.state.runs.values()]))
        logger.debug("Online devices:\n  %s", "\n  ".join([f"{dev.dev_id}: {dev.collection_state.name if dev.collection_state else 'idle'}, "
                                            f"{dev.sync_state.name if dev.sync_state else 'idle'}\n"
                                            for dev in self.state.devices.values() if dev.status == KlogDeviceStatus.online]))

    def publish(self, topic: str, payload: str, qos: int = 1, retain: bool = False):
        self.client.publish(topic, payload, qos=qos, retain=retain)
