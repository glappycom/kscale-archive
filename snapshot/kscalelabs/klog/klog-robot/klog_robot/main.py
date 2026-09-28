#!/usr/bin/env python
"""Data collection wrapper for policy deployment."""

import logging
import os
import signal
import subprocess
import time
import sys
import socket
from datetime import datetime
from pathlib import Path
import json
from prompt_toolkit import prompt
import paho.mqtt.client as mqtt
import readline
from .config import load_config
import threading
from dataclasses import dataclass, field

import colorlogging
from puid import Chars, Puid
from pytz import timezone
pacific = timezone("America/Los_Angeles")

logger = logging.getLogger(__name__)
colorlogging.configure(
    logger=logger,
    remove_existing_handlers=True,
    hide_if_not_interactive=False,
    level=logging.DEBUG,
)

cfg = load_config()

# 1 in a trillion chance of uuid conflict if we do 1 million runs
#   that's ~50 testing runs a day, every day for 50 years.
#   y'know. just in case.
id_gen: Puid = Puid(total=1e6, risk=1e15, chars=Chars.ALPHANUM_LOWER)
run_id: str = id_gen.generate()

run_dir = cfg["log_dir"] / run_id

connected = threading.Event()

@dataclass
class MessageEvent():
    msg_content: dict | None = None
    event: threading.Event = field(default_factory=threading.Event)

registered = MessageEvent()
all_ready = MessageEvent()

hostname = socket.gethostname()
client = mqtt.Client(client_id=hostname)

client.will_set(
    topic=f"device/status/{hostname}",
    payload=json.dumps({
        "device": hostname, 
        "status": "offline",
        "disconnect_type": "unexpected",
        "timestamp": time.time()
    }),
    qos=1,
)

def main(args) -> None:
    print(f"RUN_ID: {run_id}")

    logger.debug("Starting kbot data collection script with args: %s and config %s", args, cfg)
    client.connect(cfg["mqtt_host"], cfg["mqtt_port"], keepalive=60)
    client.loop_start()
    connected.wait()
    register()

    send_collecting_state("starting")

    run_dir.mkdir(parents=True, exist_ok=True)
    run_dir.chmod(0o775)

    send_start()

    # store name of kinfer file
    for arg in args.cmd:
        if arg.endswith(".kinfer"):
            kinfer_file = Path(arg).resolve()
            policy_name = kinfer_file.stem
            break
    else:
        logger.warning("No kinfer file specified. Will be logged with unknown policy.")
        kinfer_file = None


    # Holdover from old fw which used kinfer, which logged when run with these environment variables
    env: dict[str, str] = os.environ.copy()
    env["KINFER_LOG_PATH"] = run_dir.as_posix()
    env["KINFER_LOG_UUID"] = run_id

    if args.candump:
        candump_path = (run_dir / "candump.log").resolve()
        candump_cmd = f"candump -x -a -t a -H -D any > {candump_path.as_posix()}"
        logger.debug("%s", candump_cmd)
        candump_proc: subprocess.Popen[str] = subprocess.Popen(candump_cmd, text=True, shell=True)

        logger.debug("Started candump process with pid %d", candump_proc.pid)

    try:
        args.cmd.remove("--")
    except ValueError:
        pass

    output_log_path: Path = run_dir / "output.log"

    # saw slowdown when processing output with python, tee should be more performant
    # can also pin tee to a different core if needed
    cmd_string = " ".join(args.cmd) + f" | tee {str(output_log_path)} | sed 's/$/\r/'"

    logger.debug("Writing metadata")
    metadata_file: Path = run_dir / "metadata.json"
    metadata = {
            "run_id": run_id,
            "timestamp": pacific.localize(datetime.now()).isoformat(),
            "command": cmd_string,
            "policy": policy_name if kinfer_file is not None else "unknown",
            "name": args.name if args.name else "",
            "notes": args.notes if args.notes else ""
            }

    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=4)

    send_collecting_state("collecting")

    if not args.no_wait:
        logger.debug("Waiting for logging devices to be ready")
        all_ready.event.wait(timeout=10)
        if not all_ready.event.is_set():
            logger.error("Timed out waiting for devices to start collecting. Exiting.")
            shutdown()
        else:
            print(all_ready.msg_content)
            print(f"Data collection devices running: {', '.join(all_ready.msg_content['devices'])}")

    logger.debug("Running command: %s", cmd_string)
    try:
        proc: subprocess.Popen[str] = subprocess.Popen(
            cmd_string, env=env, shell=True, text=True)
        proc.wait()

    except KeyboardInterrupt:
        logger.warning("Caught Ctrl-C: Sending SIGINT to deployment process.")
        proc.send_signal(signal.SIGINT)

        try:
            proc.wait(timeout=5)
        except KeyboardInterrupt:
            logger.warning("Caught second Ctrl-C: Killing process")
            proc.kill()
            proc.wait()
        except subprocess.TimeoutExpired:
            logger.warning("Subprocess did not exit in time: Killing it.")
            proc.kill()
            proc.wait()

    logger.info("Process finished. Continuing with processing.")

    signal.signal(signal.SIGINT, ctrl_c_handler)

    if args.name is not None and not args.name.strip():
        try:
            metadata["name"] = input("Name for this run: ")
            with open(metadata_file, "w") as f:
                json.dump(metadata, f, indent=4)
        except KeyboardInterrupt:
            pass

    if args.notes is not None and not args.notes.strip():
        try:
            metadata["notes"] = prompt("Notes for this run (alt-Enter to finish):\n> ",
                                       multiline=True,
                                       prompt_continuation=lambda *_ : "> ").strip()
            with open(metadata_file, "w") as f:
                json.dump(metadata, f, indent=4)
        except KeyboardInterrupt:
            pass

    local_log = Path("events.log").resolve()
    uuid_log = Path(cfg["log_dir"] / f"{run_id}.ndjson")

    if local_log.is_file():
        logger.debug("log file found: %s", local_log)
        moved_log = save_file(local_log, "kinfer_log.ndjson")
        if moved_log is not None:
            delete_last_line(moved_log)
    elif uuid_log.is_file():
        logger.debug("log file found: %s", uuid_log)
        moved_log = save_file(uuid_log, "kinfer_log.ndjson")
    else:
        logger.error("No log file found!")

    if args.candump:
        candump_proc.terminate()
        logger.debug("Stopped candump process")

    if kinfer_file is not None:
        try:
            save_file(kinfer_file)
            logger.info("Saved kinfer file: %s", kinfer_file)

        except FileNotFoundError:
            logger.error("Kinfer file not found.")

    print(f"RUN_ID: {run_id}")
    shutdown()

def send_online() -> None:
    msg = {"device": hostname, "status": "online", "timestamp": time.time()}
    client.publish(f"device/status/{hostname}", json.dumps(msg))
    logger.info("Sent online status to MQTT broker.")

def shutdown() -> None:
    """Clean up and exit."""
    logger.info("Shutting down...")
    send_stop()
    msg = {"device": hostname, "status": "offline", "disconnect_type": "normal"}
    client.publish(f"device/status/{hostname}", json.dumps(msg))
    client.loop_stop()
    client.disconnect()
    logger.debug("Disconnected from MQTT broker.")
    sys.exit(0)

def register():
    registration_msg = {
            "device": hostname,
            "type": "klog-kbot",
            "version": "0.1.0", # TODO may be overkill
        }
    client.publish(f"device/register/{hostname}", json.dumps(registration_msg), retain=True)
    registered.event.wait(timeout=10)
    if registered.msg_content is None:
        logger.error("Failed to register with klog: No response received")
        shutdown()
    else:
        if registered.msg_content.get("status") == "confirmed":
            logger.info("Sucessfully registered with klog")

        else:
            logger.error("Failed to register with klog: %s", msg_json.get("failure_type"))
            shutdown()

@client.connect_callback()
def on_connect(client: mqtt.Client, userdata, flags, rc: int) -> None:
    topics = [
        ("logging/all_ready", 1),
        (f"device/registered/{hostname}", 1),
        ("device/scan", 1)
    ]
    if rc == 0:
        logger.info("Connected to MQTT broker at %s:%d", client._host, client._port)
        for topic in topics:
            client.subscribe(topic)
        connected.set()
    else:
        logger.error("Failed to connect to MQTT broker, return code %d", rc)

@client.message_callback()
def on_message(client: mqtt.Client, userdata: None, msg: mqtt.MQTTMessage) -> None:
    logger.debug("Received message on %s: %s", msg.topic, msg.payload.decode())
    try:
        msg_json = json.loads(msg.payload.decode())
    except json.JSONDecodeError:
        logger.error("Failed to decode JSON from message: %s", msg.payload.decode())
        return

    if msg.topic == "logging/all_ready":
        logger.debug("Received all_ready message: %s", msg_json)
        all_ready.msg_content = msg_json
        all_ready.event.set()
    elif msg.topic == f"device/registered/{hostname}":
        logger.debug("Received registration confirmation: %s", msg_json)
        registered.msg_content = msg_json
        registered.event.set()
    elif msg.topic == "device/scan":
        logger.debug("Received scan request, re-registering device.")
        register()

def save_file(file: Path, name: str | None = None) -> Path | None:
    if file.is_file():
        logger.debug("Moving file %s to %s/%s", file, run_dir, name)

        run_dir.mkdir(parents=True, exist_ok=True)
        dest = Path(run_dir / (name if name else file.name))

        try:
            dest.write_bytes(file.read_bytes())
            return dest

        except Exception as e:
            logger.error("Failed to move file %s: %s", file, e)
            return None

    else:
        logger.error("File %s not found.", file)
        return None

def delete_last_line(file: Path) -> None:
    with open(file, "r+", encoding="utf-8") as f:
        f.seek(0, os.SEEK_END)
        pos = f.tell() - 1
        while pos > 0 and f.read(1) != "\n":
            pos -= 1
            f.seek(pos, os.SEEK_SET)
        if pos > 0:
            f.seek(pos, os.SEEK_SET)
            f.truncate()

def send_start() -> None:
    msg = {"robot": hostname, "run_id": run_id}
    client.publish("logging/run/start", json.dumps(msg))

def send_collecting_state(state: str) -> None:
    msg = {"device": hostname, "run_id": run_id, "collection_state": state}
    client.publish(f"logging/collection_state/{hostname}", json.dumps(msg))

def send_stop() -> None:
    msg = {"device": hostname, "run_id": run_id}
    client.publish("logging/run/stop", json.dumps(msg))

def ctrl_c_handler(signum, frame):
    logger.info("Ctrl-C received, shutting down...")
    shutdown()
