"""
LeRobot integration for Teleop Device.

This package provides LeRobot integration for a teleoperation device
using gamepad/joystick input.
"""

from .config_teleop import TeleopConfig
from .teleop import Teleop

__version__ = "0.1.0"
__all__ = ["TeleopConfig", "Teleop"]
