import argparse
import logging
import colorlogging
from .main import main

logger = logging.getLogger(__name__)
colorlogging.configure(
    logger=logger,
    remove_existing_handlers=True,
    hide_if_not_interactive=False,
    level=logging.DEBUG,
)

def cli():
    parser = argparse.ArgumentParser(description="Wrapper script for collecting data with klog.",
                                     usage="%(prog)s [options] <COMMAND-TO-RUN>",)
    parser.add_argument("--name", "-n", type=str, nargs="?", const="",
                        help="Name for the run. Should be short. "
                        "Will be requested interactively if not provided.")
    parser.add_argument("--notes", type=str, nargs="?", const="",
                        help="Request notes for the run interactively after it's "
                        "completed.")
    parser.add_argument("--candump", "-c", action="store_true", help="Log a candump for this run")
    parser.add_argument("--no-wait", action="store_true", help="Do not wait for all collection devices to be ready before starting the run.")
    parser.add_argument("cmd", nargs=argparse.REMAINDER, help="Command to run.")
    args = parser.parse_args()
    main(args)

if __name__ == "__main__":
    cli()
