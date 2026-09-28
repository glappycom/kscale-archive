"""
LeRobot integration for Pi Camera.

This package provides LeRobot integration for the Pi camera device
with advanced features like depth sensing and IR imaging.
"""

from .config_pi import PiConfig
from .pi import Pi

__version__ = "0.1.0"
__all__ = ["PiConfig", "Pi"]
