"""Utility for logging ndjson data to rerun."""

import argparse
import logging
import sys
from pathlib import Path

import colorlogging
import rerun as rr

from telemetry.make_rerun import log_file_data
from telemetry.utils import load_joint_names

logger = logging.getLogger(__name__)


def make_rerun_from_ndjson(log_path: str, robot: str) -> None:
    """Process ndjson file and create rerun visualization."""
    log_path = Path(log_path)

    if not log_path.is_file():
        logger.error("ERROR: could not find log file at %s", log_path)
        sys.exit(2)
    logger.info("Processing log file: %s", log_path)

    # Create output file in same directory as input
    rrd_path = log_path.parent / f"{log_path.stem}.rrd"

    # Initialize rerun
    logger.info("Initializing rerun. Will save file to %s.", rrd_path)
    rr.init("kinfer-log-viewer")
    rr.save(rrd_path)

    # Log data from kinfer log file
    logger.info("Logging data into rerun")
    log_file_data(log_path, load_joint_names(robot))

    logger.info("Rerun file created: %s", rrd_path)
    logger.info("To view, run: rerun %s", rrd_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Process a kinfer log file and create a rerun visualization")
    parser.add_argument("log_path", type=str, help="Path to the kinfer log file")
    parser.add_argument("--robot", type=str, default="zbot", help="Robot name")
    args = parser.parse_args()

    make_rerun_from_ndjson(args.log_path, args.robot)


if __name__ == "__main__":
    colorlogging.configure()
    main()
