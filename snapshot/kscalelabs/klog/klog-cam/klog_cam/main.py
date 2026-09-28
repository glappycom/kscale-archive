import paho.mqtt.client as mqtt
import logging
import colorlogging
from .systemd_utils import systemd_service
from .camera import *
import json
import socket
import sys
import threading
import time
import signal

# Set up logger for this module
logger = logging.getLogger(__name__)
colorlogging.configure(
    logger=logger,
    remove_existing_handlers=True,
    hide_if_not_interactive=False,
    level=logging.DEBUG,
)

hostname = socket.gethostname()

BROKER_HOST = "klog"
BROKER_PORT = 1883
TOPICS = [
        ("logging/run/start", 1),
        ("logging/run/stop", 1),
        (f"device/registered/{hostname}", 1),
    ]

client = mqtt.Client(client_id=hostname)
client.will_set(f"device/status", json.dumps({
    "device": hostname,
    "status": "offline",
    "disconnect_type": "unexpected"}), qos=1)

class MessageEvent():
    msg: mqtt.MQTTMessage | None = None
    event: threading.Event = threading.Event()

registered = MessageEvent()
connected = threading.Event()

@systemd_service("klog-cam")
def main():
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_start()
    connected.wait()
    threading.Thread(target=register, daemon=True).start()

    logger.debug("Waiting for registration in background thread...")
    signal.signal(signal.SIGTERM, shutdown)
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
        shutdown()

def shutdown():
    logger.info("Shutting down klog-cam")
    stop_recording()
    send_disconnect()
    client.disconnect()


def register():
    logger.debug("Registering with klog")
    registration_msg = {
            "device": hostname,
            "type": "klog-cam",
            "version": "0.1.0", # TODO may be overkill
            # "cameras": 2, TODO make this work
        }
    client.publish(f"device/register/{hostname}", json.dumps(registration_msg), retain=True)

    registered.event.wait(timeout=10)

    if registered.msg is None:
        logger.error("Failed to register with klog: No response received")
        shutdown()
    else:
        msg_json = json.loads(registered.msg.payload.decode())

        if msg_json.get("status") == "confirmed":
            logger.info("Sucessfully registered with klog")

        else:
            logger.error("Failed to register with klog: %s", msg_json.get("failure_type"))
            shutdown()

def send_state(state: str, run_id: str):
    state_msg = {
        "device": hostname,
        "collection_state": state,
        "run_id": run_id
    }
    client.publish(f"logging/collection_state/{hostname}", json.dumps(state_msg), qos=1)

def send_online():
    online_msg = {
        "device": hostname,
        "status": "online",
    }
    client.publish(f"device/status/{hostname}", json.dumps(online_msg), qos=1)

def send_disconnect():
    disconnect_msg = {
        "device": hostname,
        "status": "offline",
        "disconnect_type": "normal"
    }
    client.publish(f"device/status/{hostname}", json.dumps(disconnect_msg), qos=1)

@client.message_callback()
def on_message(client, userdata, msg: mqtt.MQTTMessage):
    logger.debug("Received message on %s: %s", msg.topic, msg.payload.decode())
    msg_json = json.loads(msg.payload.decode())

    if msg.topic == f"device/checkhealth/{hostname}":
        send_online()

    elif msg.topic == f"device/registered/{hostname}":
        registered.msg = msg
        registered.event.set()

    elif msg.topic == "device/scan":
        register()

    elif msg.topic == "logging/run/start":
        logger.debug("Recieved start command. Starting cameras for run_id: %s", msg_json["run_id"])

        send_state("starting", msg_json["run_id"])
        start_recording(msg_json["run_id"])
        send_state("collecting", msg_json["run_id"])

    elif msg.topic == "logging/run/stop":
        logger.debug("Recieved stop command.")
        stop_recording()
        logger.debug("stopped recording. sending stopped message")
        send_state("done", msg_json["run_id"])

@client.connect_callback()
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT broker at %s:%d", BROKER_HOST, BROKER_PORT)
        # Subscribe to topics
        for topic, qos in TOPICS:
            client.subscribe(topic, qos)
            print(f"Subscribed to {topic} with QoS {qos}")
        connected.set()
    else:
        logger.error("Failed to connect to MQTT broker, return code %d", rc)
        sys.exit(1)

if __name__ == "__main__":
    main()
