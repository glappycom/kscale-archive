import sys
from pathlib import Path
from .make_rerun import make_rerun
import logging
import colorlogging
from .systemd_utils import systemd_service
import socket
import json
from .config import load_config
from .state import GlobalState, RunState
from .make_rerun import make_rerun
from .mqtt_manager import MqttManager
import threading

# Set up logger for this module
logger = logging.getLogger(__name__)
colorlogging.configure(
    logger=logger,
    remove_existing_handlers=True,
    hide_if_not_interactive=False,
    level=logging.DEBUG,
)

RunId = str

LOG_DIR = None

hostname = socket.gethostname()

state = GlobalState()
mqtt_manager: MqttManager | None = None

@systemd_service("klog-server", "Klog Server Service")
def main():
    global mqtt_manager, LOG_DIR
    cfg = load_config()
    LOG_DIR = cfg["log_dir"]

    state.set_callbacks(send_all_ready=send_all_ready,
                        postprocess=postprocess,
                        send_stop_run=send_stop_run,
                        send_registered=send_registered)

    mqtt_manager = MqttManager(state, hostname)
    mqtt_manager.start(cfg["mqtt_host"], cfg["mqtt_port"], keepalive=60)

def send_all_ready(run_id: RunId):
    if mqtt_manager:
        payload = json.dumps({"run_id": run_id, "status": True, "devices": state.runs[run_id].log_devices})
        mqtt_manager.publish("logging/all_ready", payload)

def send_stop_run(run_id: RunId):
    if mqtt_manager:
        payload = json.dumps({"run_id": run_id})
        mqtt_manager.publish("logging/run/stop", payload)

def send_registered(dev_id: str):
    if mqtt_manager:
        registration_msg = {
            "device": hostname,
            "status": "confirmed",
        }
        mqtt_manager.publish(f"device/registered/{dev_id}", json.dumps(registration_msg), retain=False)

def postprocess(run_id: RunId):
    logger.info(f"Postprocessing run {run_id}...")
    make_rerun(LOG_DIR / run_id)
    if run_id in state.runs:
        state.run_done(run_id)
if __name__ == "__main__":
    sys.exit(main())
