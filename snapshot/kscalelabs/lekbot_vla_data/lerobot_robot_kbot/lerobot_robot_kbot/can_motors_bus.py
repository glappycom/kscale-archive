"""
CAN Motors Bus for LeRobot integration.

This module provides a LeRobot-compatible interface for CAN-based actuators
using the pyfirmware MotorDriver system.
"""

import time
from typing import Any, Dict, List, Optional

from lerobot.motors import Motor, MotorNormMode
from lerobot.motors.motors_bus import MotorsBus

# Import your CAN system (optional dependency)
try:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent / "pyfirmware"))
    
    from firmware.can import MotorDriver
    from firmware.actuators import RobotConfig
    
    FIRMWARE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: pyfirmware not available: {e}")
    print("CAN integration will use fallback implementation")
    FIRMWARE_AVAILABLE = False
    
    # Create dummy classes for when firmware is not available
    class MotorDriver:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("pyfirmware not available. Please install pyfirmware or use a different motor interface.")
    
    class RobotConfig:
        def __init__(self):
            self.actuators = {}
            self.full_name_to_actuator_id = {}


class CANMotorsBus(MotorsBus):
    """LeRobot MotorsBus implementation for CAN-based actuators.
    
    This class wraps the pyfirmware MotorDriver to provide a LeRobot-compatible
    interface for CAN-based actuators.
    """
    
    def __init__(
        self,
        port: str,
        motors: Dict[str, Motor],
        calibration: Optional[Dict[str, Any]] = None,
        max_scaling: float = 1.0,
        joint_order: Optional[List[str]] = None,
    ):
        """Initialize the CAN Motors Bus.
        
        Args:
            port: CAN interface identifier (not used for CAN, but kept for compatibility)
            motors: Dictionary of motor configurations
            calibration: Calibration data for the motors
            max_scaling: Maximum scaling factor for motor commands
            joint_order: Order of joints for data retrieval
        """
        super().__init__(motors, calibration)
        
        self.port = port
        self.max_scaling = max_scaling
        self.joint_order = joint_order or list(motors.keys())
        
        # Initialize the CAN motor driver
        self.motor_driver: Optional[MotorDriver] = None
        self.robot_config = RobotConfig()
        
        # Create home positions from calibration or defaults
        self.home_positions = self._create_home_positions()
        
        # Track connection state
        self._connected = False
        
    def _create_home_positions(self) -> Dict[str, float]:
        """Create home positions from calibration data."""
        home_positions = {}
        
        if self.calibration:
            # Use calibration data if available
            for motor_name in self.joint_order:
                if motor_name in self.calibration:
                    home_positions[motor_name] = self.calibration[motor_name].get("home", 0.0)
                else:
                    # Use default home position from robot config
                    actuator_id = self._get_actuator_id(motor_name)
                    if actuator_id in self.robot_config.actuators:
                        home_positions[motor_name] = self.robot_config.actuators[actuator_id].default_home
        else:
            # Use default home positions from robot config
            for motor_name in self.joint_order:
                actuator_id = self._get_actuator_id(motor_name)
                if actuator_id in self.robot_config.actuators:
                    home_positions[motor_name] = self.robot_config.actuators[actuator_id].default_home
                    
        return home_positions
    
    def _get_actuator_id(self, motor_name: str) -> Optional[int]:
        """Get CAN actuator ID for a motor name."""
        if hasattr(self.robot_config, 'full_name_to_actuator_id'):
            return self.robot_config.full_name_to_actuator_id.get(motor_name)
        return None
    
    def connect(self) -> None:
        """Connect to the CAN motor system."""
        if self._connected:
            return
        
        if not FIRMWARE_AVAILABLE:
            raise RuntimeError(
                "pyfirmware is not available. Please install pyfirmware or use a different motor interface. "
                "You can install pyfirmware by running: pip install -e /path/to/pyfirmware"
            )
            
        try:
            # Initialize the motor driver
            self.motor_driver = MotorDriver(
                home_positions=self.home_positions,
                max_scaling=self.max_scaling
            )
            
            # Enable and home motors
            self.motor_driver.enable_and_home_motors()
            
            self._connected = True
            print("CAN Motors Bus connected successfully")
            
        except Exception as e:
            print(f"Failed to connect CAN Motors Bus: {e}")
            raise
    
    def disconnect(self) -> None:
        """Disconnect from the CAN motor system."""
        if not self._connected:
            return
            
        try:
            if self.motor_driver:
                # Disable motors (if there's a method for this)
                # self.motor_driver.disable_motors()  # Add this method if needed
                self.motor_driver = None
                
            self._connected = False
            print("CAN Motors Bus disconnected")
            
        except Exception as e:
            print(f"Error disconnecting CAN Motors Bus: {e}")
    
    @property
    def is_connected(self) -> bool:
        """Check if the CAN system is connected."""
        return self._connected and self.motor_driver is not None
    
    def sync_read(self, register: str) -> Dict[str, float]:
        """Read motor data synchronously.
        
        Args:
            register: Register to read (e.g., "Present_Position", "Present_Velocity")
            
        Returns:
            Dictionary mapping motor names to their values
        """
        if not self.is_connected:
            raise ConnectionError("CAN Motors Bus is not connected")
        
        try:
            # Get joint data from the motor driver
            joint_angles, joint_vels, torques, temps = self.motor_driver.get_ordered_joint_data(self.joint_order)
            
            # Map to the requested register
            if register == "Present_Position":
                return {motor: angle for motor, angle in zip(self.joint_order, joint_angles)}
            elif register == "Present_Velocity":
                return {motor: vel for motor, vel in zip(self.joint_order, joint_vels)}
            elif register == "Present_Torque":
                return {motor: torque for motor, torque in zip(self.joint_order, torques)}
            elif register == "Present_Temperature":
                return {motor: temp for motor, temp in zip(self.joint_order, temps)}
            else:
                raise ValueError(f"Unsupported register: {register}")
                
        except Exception as e:
            print(f"Error reading from CAN Motors Bus: {e}")
            raise
    
    def sync_write(self, register: str, data: Dict[str, float]) -> None:
        """Write motor data synchronously.
        
        Args:
            register: Register to write to (e.g., "Goal_Position", "Goal_Velocity")
            data: Dictionary mapping motor names to their target values
        """
        if not self.is_connected:
            raise ConnectionError("CAN Motors Bus is not connected")
        
        try:
            if register == "Goal_Position":
                # Convert to the format expected by take_action
                actions = {motor: value for motor, value in data.items() if motor in self.joint_order}
                self.motor_driver.take_action(actions)
                
                # Flush CAN buses to ensure commands are sent
                self.motor_driver.flush_can_busses()
                
            elif register == "Goal_Velocity":
                # For velocity control, you might need to implement a different approach
                # This depends on your actuator's velocity control capabilities
                print(f"Velocity control not implemented for register: {register}")
                
            else:
                raise ValueError(f"Unsupported register: {register}")
                
        except Exception as e:
            print(f"Error writing to CAN Motors Bus: {e}")
            raise
    
    def calibrate(self) -> None:
        """Calibrate the motors."""
        if not self.is_connected:
            raise ConnectionError("CAN Motors Bus is not connected")
        
        try:
            # The calibration is handled during enable_and_home_motors()
            # You might want to add additional calibration steps here
            print("CAN Motors calibration completed")
            
        except Exception as e:
            print(f"Error calibrating CAN Motors Bus: {e}")
            raise
    
    def get_motor_info(self, motor_name: str) -> Dict[str, Any]:
        """Get information about a specific motor.
        
        Args:
            motor_name: Name of the motor
            
        Returns:
            Dictionary containing motor information
        """
        if motor_name not in self.joint_order:
            raise ValueError(f"Unknown motor: {motor_name}")
        
        actuator_id = self._get_actuator_id(motor_name)
        if actuator_id is None:
            return {"name": motor_name, "status": "unknown"}
        
        if actuator_id in self.robot_config.actuators:
            actuator = self.robot_config.actuators[actuator_id]
            return {
                "name": motor_name,
                "can_id": actuator_id,
                "actuator_type": actuator.actuator_type.name,
                "default_home": actuator.default_home,
                "kp": actuator.kp,
                "kd": actuator.kd,
                "status": "configured"
            }
        
        return {"name": motor_name, "status": "not_found"}
    
    def get_all_motor_info(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all motors.
        
        Returns:
            Dictionary mapping motor names to their information
        """
        return {motor_name: self.get_motor_info(motor_name) for motor_name in self.joint_order}
