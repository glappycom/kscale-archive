"""
Motor mapping utilities for CAN actuators.

This module provides utilities for mapping between LeRobot motor interface
and CAN-based actuators from the pyfirmware system.
"""

from typing import Dict, List, Optional, Tuple

# Import your CAN system
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent / "pyfirmware"))

from firmware.actuators import RobotConfig, ActuatorConfig


class CANMotorMapper:
    """Maps between LeRobot motor interface and CAN actuators."""
    
    def __init__(self, robot_config: Optional[RobotConfig] = None):
        """Initialize the motor mapper.
        
        Args:
            robot_config: Robot configuration from pyfirmware
        """
        self.robot_config = robot_config or RobotConfig()
        self._joint_to_can_id: Dict[str, int] = {}
        self._can_id_to_joint: Dict[int, str] = {}
        
        # Build mapping dictionaries
        self._build_mappings()
    
    def _build_mappings(self) -> None:
        """Build mappings between joint names and CAN IDs."""
        for actuator_id, actuator in self.robot_config.actuators.items():
            joint_name = actuator.full_name
            self._joint_to_can_id[joint_name] = actuator_id
            self._can_id_to_joint[actuator_id] = joint_name
    
    def get_can_id(self, joint_name: str) -> Optional[int]:
        """Get CAN ID for a joint name.
        
        Args:
            joint_name: Name of the joint
            
        Returns:
            CAN ID if found, None otherwise
        """
        return self._joint_to_can_id.get(joint_name)
    
    def get_joint_name(self, can_id: int) -> Optional[str]:
        """Get joint name for a CAN ID.
        
        Args:
            can_id: CAN ID of the actuator
            
        Returns:
            Joint name if found, None otherwise
        """
        return self._can_id_to_joint.get(can_id)
    
    def get_actuator_config(self, joint_name: str) -> Optional[ActuatorConfig]:
        """Get actuator configuration for a joint.
        
        Args:
            joint_name: Name of the joint
            
        Returns:
            Actuator configuration if found, None otherwise
        """
        can_id = self.get_can_id(joint_name)
        if can_id is not None:
            return self.robot_config.actuators.get(can_id)
        return None
    
    def get_joint_limits(self, joint_name: str) -> Optional[Tuple[float, float]]:
        """Get joint limits for a joint.
        
        Args:
            joint_name: Name of the joint
            
        Returns:
            Tuple of (min_angle, max_angle) if found, None otherwise
        """
        actuator = self.get_actuator_config(joint_name)
        if actuator is not None:
            return (actuator.angle_can_min, actuator.angle_can_max)
        return None
    
    def get_pid_parameters(self, joint_name: str) -> Optional[Tuple[float, float]]:
        """Get PID parameters for a joint.
        
        Args:
            joint_name: Name of the joint
            
        Returns:
            Tuple of (kp, kd) if found, None otherwise
        """
        actuator = self.get_actuator_config(joint_name)
        if actuator is not None:
            return (actuator.kp, actuator.kd)
        return None
    
    def get_all_joints(self) -> List[str]:
        """Get all joint names.
        
        Returns:
            List of all joint names
        """
        return list(self._joint_to_can_id.keys())
    
    def get_all_can_ids(self) -> List[int]:
        """Get all CAN IDs.
        
        Returns:
            List of all CAN IDs
        """
        return list(self._can_id_to_joint.keys())
    
    def create_joint_order(self, joint_names: List[str]) -> List[str]:
        """Create a joint order that matches the robot configuration.
        
        Args:
            joint_names: List of joint names to order
            
        Returns:
            Ordered list of joint names
        """
        # Filter to only include joints that exist in the robot config
        valid_joints = [name for name in joint_names if name in self._joint_to_can_id]
        
        # Sort by CAN ID to ensure consistent ordering
        valid_joints.sort(key=lambda name: self._joint_to_can_id[name])
        
        return valid_joints
    
    def validate_joint_names(self, joint_names: List[str]) -> Tuple[List[str], List[str]]:
        """Validate joint names against the robot configuration.
        
        Args:
            joint_names: List of joint names to validate
            
        Returns:
            Tuple of (valid_joints, invalid_joints)
        """
        valid_joints = []
        invalid_joints = []
        
        for joint_name in joint_names:
            if joint_name in self._joint_to_can_id:
                valid_joints.append(joint_name)
            else:
                invalid_joints.append(joint_name)
        
        return valid_joints, invalid_joints
    
    def get_actuator_info(self, joint_name: str) -> Optional[Dict[str, any]]:
        """Get comprehensive actuator information.
        
        Args:
            joint_name: Name of the joint
            
        Returns:
            Dictionary containing actuator information
        """
        actuator = self.get_actuator_config(joint_name)
        if actuator is None:
            return None
        
        return {
            "joint_name": joint_name,
            "can_id": actuator.can_id,
            "actuator_type": actuator.actuator_type.name,
            "default_home": actuator.default_home,
            "kp": actuator.kp,
            "kd": actuator.kd,
            "angle_limits": (actuator.angle_can_min, actuator.angle_can_max),
            "velocity_limits": (actuator.velocity_can_min, actuator.velocity_can_max),
            "torque_limits": (actuator.torque_can_min, actuator.torque_can_max),
        }
    
    def get_all_actuator_info(self) -> Dict[str, Dict[str, any]]:
        """Get information about all actuators.
        
        Returns:
            Dictionary mapping joint names to their information
        """
        return {
            joint_name: self.get_actuator_info(joint_name)
            for joint_name in self.get_all_joints()
        }
