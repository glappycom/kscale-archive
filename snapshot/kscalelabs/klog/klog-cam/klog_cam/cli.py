import sys
import logging
import colorlogging
from .camera import *

# Set up logger for this module
logger = logging.getLogger(__name__)
colorlogging.configure(
    logger=logger,
    remove_existing_handlers=True,
    hide_if_not_interactive=False,
    level=logging.DEBUG,
)

def main():
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} <command>")
        print("Available commands: start, stop, setup, preview, adjust")
        sys.exit(1)

    command = sys.argv[1]

    if command.startswith("rec") or command == "start":
        if len(sys.argv) != 3:
            print("usage: klog_cam start <run_id>")
            sys.exit(1)
        logger.debug(f"Starting recording with run_id: {sys.argv[2]}")
        start_recording(sys.argv[2])
        logger.debug(f"Started recording")

    elif command.startswith("stop_rec") or command == "stop":
        stop_recording()

    elif command == "setup":
        setup_camera()

    elif command == "adjust":
        if len(sys.argv) != 3:
            print("usage: klog_cam adjust <target_ip>")
            sys.exit(1)
        adjust_camera(sys.argv[2])

    elif command == "preview":
        if len(sys.argv) != 3:
            print("usage: klog_cam preview <target_ip>")
            sys.exit(1)
        preview_camera(sys.argv[2])

    else:
        print(f"Unknown command: {command}")
        print("Available commands: start, stop, setup, preview")
        sys.exit(1)


if __name__ == "__main__":
    main()
