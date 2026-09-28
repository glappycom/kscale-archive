import subprocess
import logging
import colorlogging
import klog_cam.scripts
import importlib.resources as pkg_resources
import sys

__all__ = [
    "start_recording",
    "stop_recording",
    "setup_camera",
    "adjust_camera",
    "preview_camera",
]

# Set up logger for this module
logger = logging.getLogger(__name__)
colorlogging.configure(
    logger=logger,
    remove_existing_handlers=True,
    hide_if_not_interactive=False,
    level=logging.DEBUG,
)

# TODO move most of the camera logic here, just leaving ffmpeg stuff in script. refactor
def start_recording(run_id: str) -> str | None:
    with pkg_resources.path(klog_cam.scripts, "klog_cam_start") as script:
        try:
            proc = subprocess.run([script, run_id], check=True)
            if proc.returncode != 0:
                logger.error(f"Failed to start recording with run_id {run_id}. Return code: {proc.returncode}")
                return str(proc.returncode)
            else:
                logger.debug(f"Started recording with run_id: {run_id}")
                return None
        except Exception as e:
            logger.error(f"Failed to start recording: {e}")
            return str(e)


def stop_recording() -> str | None:
    with pkg_resources.path(klog_cam.scripts, "klog_cam_stop") as script:
        try:
            subprocess.run([script], check=True)
            logger.debug(f"Stopped recording.")
            return None
        except Exception as e:
            logger.error(f"Failed to stop recording: {e}")
            return str(e)


def setup_camera():
    with pkg_resources.path(klog_cam.scripts, "klog_cam_setup") as script:
        subprocess.run([script], check=True)


def adjust_camera(target_ip: str):
    with (
        pkg_resources.path(klog_cam.scripts, "klog_cam_adjust") as adjust,
        pkg_resources.path(klog_cam.scripts, "klog_cam_preview") as preview,
    ):
        preview_proc = subprocess.Popen([preview, target_ip])

        try:
            subprocess.run([adjust, target_ip], check=True)
        finally:
            preview_proc.terminate()
            preview_proc.wait()


def preview_camera(target_ip: str):
    with pkg_resources.path(klog_cam.scripts, "klog_cam_preview") as script:
        subprocess.run([script, target_ip, target_ip], check=True)
