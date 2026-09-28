import socket
import paho.mqtt.client as mqtt
import json
from .SyncManager import SyncManager
from .config import load_config
from .systemd_utils import systemd_service
import logging
import colorlogging
from pathlib import Path
import sys
import time

logger = logging.getLogger(__name__)
colorlogging.configure(
    logger=logger,
    remove_existing_handlers=True,
    hide_if_not_interactive=False,
    level=logging.DEBUG,
)

hostname = socket.gethostname()

TOPICS = [
        ("logging/run/start", 1),
        ("logging/run/stop", 1),
    ]

# unique client ID
client = mqtt.Client(client_id=f"{hostname}_sync")

client.will_set(
    topic=f"device/status/{hostname}",
    payload=json.dumps({
        "device": hostname + "_sync", 
        "status": "offline",
        "disconnect_type": "unexpected",
        "timestamp": time.time()
    }),
    qos=1,
)

syncer: SyncManager = SyncManager()

RunId = str

@systemd_service("klog-sync", description="Klog sync daemon")
def main():
    global syncer
    cfg = load_config()
    client.connect(cfg["mqtt_host"], cfg["mqtt_port"], keepalive=60)

    dst = f"rsync://{cfg['remote_user']}@{cfg['remote_host']}/{cfg['rsync_module']}"
    syncer.new(src=cfg["source_dir"],
               dst=dst,
               max_dir_size=cfg["max_dir_size"],
               min_remaining_disk_space=cfg["min_remaining_disk_space"],
               sync_state_changed_callback=send_sync_state)
    client.loop_forever()

def send_sync_state(run_id: RunId, state: str, failure_type: str | None = None):
    msg = {
        "run_id": run_id,
        "device": hostname,
        "sync_state": state,
        "failure_type": failure_type,
    }
    topic = f"logging/sync_state/{hostname}"
    client.publish(topic, json.dumps(msg), qos=1)
    logger.info("Published sync state for run %s: %s", run_id, state)

@client.message_callback()
def on_message(client, userdata, msg: mqtt.MQTTMessage):
    logger.debug("Received message on %s: %s", msg.topic, msg.payload.decode())
    msg_json = json.loads(msg.payload.decode())
    
    if msg.topic == "logging/run/start":
        logger.debug("Run started: %s", msg.payload.decode())
        syncer.pause()

    elif msg.topic == "logging/run/stop":
        logger.debug("Run stopped: %s", msg.payload.decode())
        syncer.queue(msg_json["run_id"])
        syncer.sync()
    
@client.connect_callback()
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT broker at %s:%d", client._host, client._port)
        for topic in TOPICS:
            client.subscribe(topic)
    else:
        logger.error("Failed to connect to MQTT broker, return code %d", rc)

if __name__ == "__main__":
    main()
