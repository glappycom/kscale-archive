"""
LeRobot integration for KBot Robot.

This package provides LeRobot integration for the KBot robot arm
using Feetech servos.
"""

from .config_kbot import KBotConfig
from .kbot import KBot

__version__ = "0.1.0"
__all__ = ["KBotConfig", "KBot"]
