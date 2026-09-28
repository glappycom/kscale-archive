"""
Configuration class for Pi Camera.

This module defines the configuration options for the Pi camera device.
"""

from dataclasses import dataclass

from lerobot.cameras.config import CameraConfig


@CameraConfig.register_subclass("pi")
@dataclass
class PiConfig(CameraConfig):
    """Configuration for Pi Camera.
    
    This configuration class defines the parameters needed to connect
    and control the Pi camera device.
    
    Args:
        device_id: Camera device ID or path
        width: Image width (default: 640)
        height: Image height (default: 480)
        fps: Frames per second (default: 30)
        depth_enabled: Enable depth sensing (default: True)
        ir_enabled: Enable IR imaging (default: False)
    """
    device_id: str = "0"
    width: int = 640
    height: int = 480
    fps: int = 30
    depth_enabled: bool = True
    ir_enabled: bool = False
