"""
Configuration class for Teleop Device.

This module defines the configuration options for the teleoperation device.
"""

from dataclasses import dataclass

from lerobot.teleoperators.config import TeleoperatorConfig


@TeleoperatorConfig.register_subclass("teleop")
@dataclass
class TeleopConfig(TeleoperatorConfig):
    """Configuration for Teleop Device.
    
    This configuration class defines the parameters needed to connect
    and control the teleoperation device.
    
    Args:
        port: Network port or device path for communication
        deadzone: Joystick deadzone threshold (default: 0.1)
        max_speed: Maximum speed scaling factor (default: 1.0)
    """
    port: str = "192.168.1.1"
    deadzone: float = 0.1
    max_speed: float = 1.0
