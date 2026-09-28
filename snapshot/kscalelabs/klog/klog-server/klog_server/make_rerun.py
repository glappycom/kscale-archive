"""Rerun log generation utilities for telemetry data."""

import json
import logging
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence

import colorlogging
import numpy as np
import numpy.typing as npt
import rerun as rr
from pytz import timezone, utc
import zipfile

from .utils import load_joint_names

import os
import stat
import pwd
import grp

# Set up logger for this module
logger = logging.getLogger(__name__)
colorlogging.configure(
    logger=logger,
    remove_existing_handlers=True,
    hide_if_not_interactive=False,
    level=logging.DEBUG,
)

pacific = timezone("America/Los_Angeles")

def make_rerun(run_dir: Path) -> None:
    print(f"Current user: {pwd.getpwuid(os.getuid()).pw_name}")
    print(f"Current groups: {[grp.getgrgid(gid).gr_name for gid in os.getgroups()]}")
    print(f"Directory exists: {os.path.exists('/mnt/klog1')}")
    print(f"Directory writable: {os.access('/mnt/klog1', os.W_OK)}")
    
    logger.debug("Rerun version: %s", rr.__version__)

    run_dir = run_dir.resolve()

    if not run_dir.is_dir():
        logger.error("Run directory %s does not exist or is not a directory.", run_dir)
        sys.exit(2)

    logger.info("Creating rerun file with data from %s", run_dir)

    run_id: str = run_dir.name

    logger.debug("Target directory for this run: %s", run_dir)
    log_path: Path = run_dir / "kinfer_log.ndjson"

    if log_path.is_file():
        logger.debug("Log file found: %s", log_path)

    else:
        logger.error("No log file found!")
        return

    rrd_path: Path = run_dir / "run.rrd"

    ## Rerun things
    logger.debug("Initializing rerun. Will save file to %s.", rrd_path)
    rr.init("kbot-deployments", recording_id=run_id)
    rr.save(rrd_path)

    run_info_path: Path = run_dir / "metadata.json"
    run_info_text = run_info_path.read_text() if run_info_path.is_file() else "{}"
    run_info = json.loads(run_info_text)
    run_start_time: datetime = datetime.strptime(run_info["timestamp"], "%Y-%m-%dT%H:%M:%S.%f%z")

    logger.debug("Logging run info from %s: %s", run_info_path, run_info_text)

    rr.set_time("time", timestamp=run_start_time.timestamp())
    rr.log("run_info", rr.TextDocument(run_info_text))

    kinfer_files = list(run_dir.glob("*.kinfer"))

    if len(kinfer_files) == 1:
        kinfer_file: Path = kinfer_files[0]
        joint_names: Sequence[str] = load_joint_names(kinfer_file)
    else:
        logger.warning("Expected exactly one kinfer file, found %d. Will use default joint names.", len(kinfer_files))
        joint_names = None

    # Log data from kinfer log file
    logger.debug("Logging data into rerun")
    log_file_data(log_path, joint_names)

    log_path: Path = run_dir / "output.log"
    if log_path.is_file():
        logger.info("Logging terminal output")
        log_output(log_path)

    # Log candump data
    candump_path: Path = run_dir / "candump.log"
    if candump_path.is_file():
        logger.info("Logging candump data")
        log_candump(candump_path)

    # Log video data
    for vid_path in run_dir.glob("*.mp4"):
        log_video_data(vid_path)

    script_path = Path(__file__).resolve()
    project_src = script_path.parent
    rbl_path = project_src / "assets" / "kbot-deployments.rbl"
    rr.log_file_from_path(rbl_path)

    # Compact file
    logger.info("Compacting rerun file.")
    subprocess.run(f"rerun rrd compact {str(rrd_path)} -o {str(rrd_path)}", check=True, shell=True)

    logger.info("Finished compacting. Rerun file is ready.")

    zip_path: Path = run_dir / f"{run_id}.zip"
    logger.info("Zipping data to %s", zip_path)
    with zipfile.ZipFile(zip_path, "w") as zip_file:
        for f in run_dir.iterdir():
            logger.debug("Adding %s to zip", f)
            if f.is_file() and not f.suffix.endswith("zip") and not f.name.startswith("."):
                zip_file.write(str(f))
    logger.info("Zip file ready.")

    logger.info("Make rerun completed successfully. Rerun file: %s", rrd_path)

def get_timestamps(vid_path: Path) -> list[datetime]:
    with open(vid_path.with_suffix(".txt")) as f:
        next(f)  # skip first line which isn't a timestamp
        datetimes: list[datetime] = [
            datetime.fromtimestamp(int(line.strip()) / 1e6, tz=utc).astimezone(pacific) for line in f if line.strip()
        ]
    return datetimes

def log_video_data(vid_path: Path) -> None:
    real_timestamps: list[datetime] = get_timestamps(vid_path)
    logger.info("Adding video: %s", vid_path)
    cam_entity_path: str = "video/" + vid_path.stem
    vid_asset: rr.AssetVideo = rr.AssetVideo(path=vid_path)
    rr.log(cam_entity_path, vid_asset, static=True)

    vid_timestamps_ns: npt.NDArray[np.int64] = vid_asset.read_frame_timestamps_nanos()

    for timestamp, frame_ns in zip(real_timestamps, vid_timestamps_ns):
        rr.set_time("time", timestamp=timestamp)
        rr.log(cam_entity_path, rr.VideoFrameReference(nanoseconds=int(frame_ns)))

def log_candump(candump_path: Path) -> None:
    logger.info("Logging CAN dump data from %s", candump_path)

    timestamp_regex = re.compile(r"\((\d+\.\d+)\)")

    with open(candump_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # skip empty lines
            match = timestamp_regex.match(line)
            if match:
                timestamp_str = match.group(1)
            else:
                logger.warning("Could not parse timestamp from line: %s", line.strip())
                continue

            timestamp = float(timestamp_str)

            rr.set_time("can_time", timestamp=timestamp)

            rr.log("logs/can", rr.TextLog(line, level="INFO"))

def strip_color_codes(text: str) -> str:
    ansi_escape_pattern = re.compile(r"\x1b\[[0-9;]*m")
    return ansi_escape_pattern.sub("", text)


def log_output(output_path: Path) -> None:
    logger.info("Logging terminal output from %s", output_path)

    with open(output_path, "r") as f:
        for line in f:
            line = strip_color_codes(line.strip())
            if not line:
                continue  # skip empty lines

            timestamp_str = line.split(" ", 1)[0]

            try:
                dt = datetime.fromisoformat(timestamp_str)

            except Exception as e:
                logger.warning("Could not parse timestamp from string: %s: %s", timestamp_str, e)
                continue

            rr.set_time("time", timestamp=dt.timestamp())

            rr.log("logs/firmware", rr.TextLog(line, level="INFO"))


def log_file_data(log_path: Path, joint_names: Sequence[str] | None) -> None:
    if joint_names is None:
        joint_names = [f"joint_{i}" for i in range(20)]
    else:
        joint_names = ["_".join(name.split("_")[1:-1]) for name in joint_names]

    # Data from log file
    data_lines: list[dict[str, Any]] = []
    with open(log_path, "r") as f:
        for line in f:
            try:
                data_lines.append(json.loads(line))
            except json.decoder.JSONDecodeError:
                logger.warning("Failed to parse json line: %s", line)

    line_count = 0

    logger.debug("Loding stl")

    script_path = Path(__file__).resolve()
    project_src = script_path.parent
    stl_path = project_src / "assets" / "car.stl"

    rr.log("imu/quaternion", rr.Asset3D(path=stl_path), static=True)

    logger.debug("Attempting to log %d lines from %s", len(data_lines), log_path)

    line_count = 0

    for data in data_lines:
        time_us: Any = data.pop("t_us")
        time: float = float(time_us) / 1e6
        rr.set_time("time", timestamp=time)

        for key, value in data.items():
            # logger.debug("Logging %s: %s", key, value)

            if value is None:
                continue

            # Joint info
            if key == "joint_angles":
                for i, val in enumerate(value):
                    if i < len(joint_names):
                        rr.log(f"joints/{joint_names[i]}/real_pos", rr.Scalars([float(val)]))

                    else:
                        logger.warning("Index %d out of range for joint_names. Skipping logging for %s.", i, key)

            elif key == "joint_vels":
                for i, val in enumerate(value):
                    if i < len(joint_names):
                        rr.log(f"joints/{joint_names[i]}/real_vel", rr.Scalars([float(val)]))
                    else:
                        logger.warning("Index %d out of range for joint_names. Skipping logging for %s.", i, key)

            # Control
            elif key == "command":
                for i, val in enumerate(value):
                    if i < len(joint_names):
                        rr.log(f"commands/{i}", rr.Scalars([float(val)]))


            elif key == "output":
                for i, val in enumerate(value):
                    if i < len(joint_names):
                        rr.log(f"joints/{joint_names[i]}/command_pos", rr.Scalars([float(val)]))
                    else:
                        logger.warning("Index %d out of range for joint_names. Skipping logging for %s.", i, key)

            elif key == "joint_amps":
                for i, val in enumerate(value):
                    if i < len(joint_names):
                        rr.log(f"joints/{joint_names[i]}/current", rr.Scalars([float(val)]))
                    else:
                        logger.warning("Index %d out of range for joint_names. Skipping logging for %s.", i, key)

            elif key.startswith("joint_"):
                prop_name = key.split("_", 1)[1]
                for i, val in enumerate(value):
                    if i < len(joint_names):
                        rr.log(f"joints/{joint_names[i]}/{prop_name}", rr.Scalars([float(val)]))
                    else:
                        logger.warning("Index %d out of range for joint_names. Skipping logging for %s.", i, key)

            # Sensors
            elif key == "projected_g":
                scalar_values = [float(v) for v in value]
                rr.log("imu/projected_g_comps", rr.Scalars(scalar_values))
                rr.log("imu/projected_g", rr.Arrows3D(vectors=[scalar_values]))
            elif key == "accel":
                scalar_values = [float(v) for v in value]
                rr.log("imu/accel_comps", rr.Scalars(scalar_values))
                rr.log("imu/accel", rr.Arrows3D(vectors=[scalar_values]))
            elif key == "gyro":
                scalar_values = [float(v) for v in value]
                rr.log("imu/gyro_comps", rr.Scalars(scalar_values))
                rr.log("imu/gyro", rr.Arrows3D(vectors=[scalar_values]))
            elif key == "quaternion":
                wxyz = [float(v) for v in value]
                xyzw = [wxyz[1], wxyz[2], wxyz[3], wxyz[0]]
                rr.log("imu/quaternion", rr.Transform3D(rotation=rr.Quaternion(xyzw=xyzw)))
                rr.log("imu/quaternion", rr.Arrows3D(origins=[0,0,0], vectors=[0,0,1]))
                rr.log(f"imu/quat_comps (wxyz)", rr.Scalars(wxyz))

            # Catch-all, everything else goes in sensors
            elif isinstance(value, (list, tuple)):
                scalar_values = [float(v) for v in value]
                rr.log(f"sensors/{key}", rr.Scalars(scalar_values))
            else:
                rr.log(f"sensors/{key}", rr.Scalars([float(value)]))

        line_count += 1

    logger.info("Logged %d lines", line_count)


def main():
    try:
        run_dir: Path = Path(sys.argv[1].strip())
    except IndexError:
        logger.error("usage: python make_rerun.py <UUID>")
        return

    make_rerun(run_dir)

if __name__ == "__main__":
    main()
