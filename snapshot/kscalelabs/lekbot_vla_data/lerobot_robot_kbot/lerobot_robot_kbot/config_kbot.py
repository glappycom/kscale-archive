"""
Configuration class for KBot Robot.

This module defines the configuration options for the KBot robot arm.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from lerobot.cameras import CameraConfig
from lerobot.cameras.opencv import OpenCVCameraConfig
from lerobot.robots import RobotConfig


@RobotConfig.register_subclass("kbot_parallel")
@dataclass
class KBotConfig(RobotConfig):
    """Configuration for KBot Robot with CAN-based actuators.
    
    This configuration class defines the parameters needed to connect
    and control the KBot robot with CAN-based actuators.
    
    Args:
        port: CAN interface identifier (not used for CAN, but kept for compatibility)
        left_arm_ids: CAN IDs for left arm actuators
        right_arm_ids: CAN IDs for right arm actuators
        left_arm_names: Names for left arm joints
        right_arm_names: Names for right arm joints
        max_scaling: Maximum scaling factor for motor commands (default: 1.0)
        joint_order: Order of joints for data retrieval
        cameras: Dictionary of camera configurations
    """
    port: str = "can0"  # CAN interface identifier
    
    # CAN actuator configuration - all 22 actuators from RobotConfig
    # Left arm (6 actuators)
    left_arm_ids: List[int] = field(default_factory=lambda: [11, 12, 13, 14, 15, 16])
    left_arm_names: List[str] = field(default_factory=lambda: [
        "dof_left_shoulder_pitch_03",
        "dof_left_shoulder_roll_03",
        "dof_left_shoulder_yaw_02",
        "dof_left_elbow_02",
        "dof_left_wrist_00",
        "dof_left_wrist_gripper_05",
    ])
    
    # Right arm (6 actuators)
    right_arm_ids: List[int] = field(default_factory=lambda: [21, 22, 23, 24, 25, 26])
    right_arm_names: List[str] = field(default_factory=lambda: [
        "dof_right_shoulder_pitch_03",
        "dof_right_shoulder_roll_03",
        "dof_right_shoulder_yaw_02",
        "dof_right_elbow_02",
        "dof_right_wrist_00",
        "dof_right_wrist_gripper_05",
    ])
    
    # Left leg (5 actuators)
    left_leg_ids: List[int] = field(default_factory=lambda: [31, 32, 33, 34, 35])
    left_leg_names: List[str] = field(default_factory=lambda: [
        "dof_left_hip_pitch_04",
        "dof_left_hip_roll_03",
        "dof_left_hip_yaw_03",
        "dof_left_knee_04",
        "dof_left_ankle_02",
    ])
    
    # Right leg (5 actuators)
    right_leg_ids: List[int] = field(default_factory=lambda: [41, 42, 43, 44, 45])
    right_leg_names: List[str] = field(default_factory=lambda: [
        "dof_right_hip_pitch_04",
        "dof_right_hip_roll_03",
        "dof_right_hip_yaw_03",
        "dof_right_knee_04",
        "dof_right_ankle_02",
    ])

    # CAN-specific parameters
    max_scaling: float = 1.0
    joint_order: Optional[List[str]] = None
    
    # Camera configuration - matches zbot-record19 dataset format
    cameras: Dict[str, CameraConfig] = field(default_factory=lambda: {
        "front": OpenCVCameraConfig(
            index_or_path=0,  # Default camera index
            fps=60,  # Match dataset FPS
            width=320,  # Match dataset width
            height=240,  # Match dataset height
        ),
    })