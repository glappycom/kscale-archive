"""
KBot Robot implementation.

This module implements the LeRobot Robot interface for the KBot robot arm
using CAN-based actuators.
"""

from typing import Any, Dict, List

from lerobot.cameras import make_cameras_from_configs
from lerobot.motors import Motor, MotorNormMode
from lerobot.robots import Robot

from .config_kbot import KBotConfig
from .can_motors_bus import CANMotorsBus, FIRMWARE_AVAILABLE
from .alternative_motors_bus import SimulatedMotorsBus, SerialMotorsBus


class KBot(Robot):
    """KBot Robot - A dual-arm robot with CAN-based actuators.
    
    This robot implementation provides:
    - Dual-arm control using CAN-based actuators
    - Camera support for visual feedback
    - Real-time position control
    - Calibration and configuration support
    """
    
    config_class = KBotConfig
    name = "kbot_parallel"

    def __init__(self, config: KBotConfig):
        """Initialize the robot with the given configuration.
        
        Args:
            config: Robot configuration containing CAN parameters, cameras, etc.
        """
        super().__init__(config)
        
        # Create joint order from left and right arm names
        self.joint_order = self._create_joint_order()
        
        # Create motor configurations for CAN actuators
        motors = self._create_motor_configs()
        
        # Initialize the appropriate motors bus based on availability
        if FIRMWARE_AVAILABLE:
            # Use CAN motors bus with pyfirmware
            self.bus = CANMotorsBus(
                port=self.config.port,
                motors=motors,
                calibration=self.calibration,
                max_scaling=self.config.max_scaling,
                joint_order=self.joint_order,
            )
        else:
            # Use alternative motor bus (simulated or serial)
            if self.config.port.startswith("sim"):
                # Use simulated motors for testing
                self.bus = SimulatedMotorsBus(
                    port=self.config.port,
                    motors=motors,
                    calibration=self.calibration,
                    max_scaling=self.config.max_scaling,
                    joint_order=self.joint_order,
                )
            else:
                # Use serial motors for real hardware
                self.bus = SerialMotorsBus(
                    port=self.config.port,
                    motors=motors,
                    calibration=self.calibration,
                    baudrate=115200,  # Default baudrate
                    joint_order=self.joint_order,
                )
        
        # Initialize cameras
        self.cameras = make_cameras_from_configs(config.cameras)
    
    def _create_joint_order(self) -> List[str]:
        """Create the joint order from all actuator names."""
        return (
            self.config.left_arm_names + 
            self.config.right_arm_names +
            self.config.left_leg_names +
            self.config.right_leg_names
        )
    
    def _create_motor_configs(self) -> Dict[str, Motor]:
        """Create motor configurations for CAN actuators.
        
        Returns:
            Dictionary mapping joint names to Motor objects
        """
        motors = {}
        
        # Create motors for left arm (6 actuators)
        for joint_name, can_id in zip(self.config.left_arm_names, self.config.left_arm_ids):
            motors[joint_name] = Motor(
                can_id,  # Use CAN ID as motor ID
                "can_actuator",  # Motor type identifier
                MotorNormMode.RANGE_M100_100,  # Normalized range
            )
        
        # Create motors for right arm (6 actuators)
        for joint_name, can_id in zip(self.config.right_arm_names, self.config.right_arm_ids):
            motors[joint_name] = Motor(
                can_id,  # Use CAN ID as motor ID
                "can_actuator",  # Motor type identifier
                MotorNormMode.RANGE_M100_100,  # Normalized range
            )
        
        # Create motors for left leg (5 actuators)
        for joint_name, can_id in zip(self.config.left_leg_names, self.config.left_leg_ids):
            motors[joint_name] = Motor(
                can_id,  # Use CAN ID as motor ID
                "can_actuator",  # Motor type identifier
                MotorNormMode.RANGE_M100_100,  # Normalized range
            )
        
        # Create motors for right leg (5 actuators)
        for joint_name, can_id in zip(self.config.right_leg_names, self.config.right_leg_ids):
            motors[joint_name] = Motor(
                can_id,  # Use CAN ID as motor ID
                "can_actuator",  # Motor type identifier
                MotorNormMode.RANGE_M100_100,  # Normalized range
            )
        
        return motors

    @property
    def _motors_ft(self) -> Dict[str, type]:
        """Motor features for observation and action."""
        return {
            joint_name: float for joint_name in self.joint_order
        }
    
    @property
    def _motors_pos_ft(self) -> Dict[str, type]:
        """Motor position features for observation and action."""
        return {
            f"{joint_name}.pos": float for joint_name in self.joint_order
        }
    
    @property
    def _motors_vel_ft(self) -> Dict[str, type]:
        """Motor velocity features for observation."""
        return {
            f"{joint_name}.vel": float for joint_name in self.joint_order
        }

    @property
    def _cameras_ft(self) -> Dict[str, tuple]:
        """Camera features for observation."""
        return {
            f"images.{cam}": (self.cameras[cam].height, self.cameras[cam].width, 3) 
            for cam in self.cameras
        }

    @property
    def observation_features(self) -> Dict[str, Any]:
        """Define the structure of sensor outputs from the robot.
        
        Returns:
            Dictionary describing observation features including motor positions,
            velocities, and camera images.
        """
        return {
            **self._motors_pos_ft,  # Position features
            **self._motors_vel_ft,  # Velocity features
            **self._cameras_ft      # Camera features
        }

    @property
    def action_features(self) -> Dict[str, Any]:
        """Define the structure of action commands for the robot.
        
        Returns:
            Dictionary describing action features for motor control.
        """
        return self._motors_pos_ft

    def connect(self) -> None:
        """Connect to the robot hardware."""
        if self.is_connected:
            return
            
        # Connect to the CAN motors bus
        self.bus.connect()
        
        # Connect cameras
        for cam in self.cameras.values():
            cam.connect()

    def disconnect(self) -> None:
        """Disconnect from the robot hardware."""
        if not self.is_connected:
            return
            
        # Disconnect CAN motors bus
        self.bus.disconnect()
        
        # Disconnect cameras
        for cam in self.cameras.values():
            cam.disconnect()

    @property
    def is_connected(self) -> bool:
        """Check if the robot is connected."""
        return self.bus.is_connected and all(
            cam.is_connected for cam in self.cameras.values()
        )

    def get_observation(self) -> Dict[str, Any]:
        """Get current sensor readings from the robot.
        
        Returns:
            Dictionary containing motor positions, velocities, and camera images.
            
        Raises:
            ConnectionError: If robot is not connected.
        """
        if not self.is_connected:
            raise ConnectionError(f"{self} is not connected.")

        # Read motor positions and velocities from CAN bus
        positions = self.bus.sync_read("Present_Position")
        velocities = self.bus.sync_read("Present_Velocity")
        
        # Format observations to match dataset structure
        obs_dict = {}
        
        # Add position and velocity data with proper naming
        for joint_name in self.joint_order:
            obs_dict[f"{joint_name}.pos"] = positions.get(joint_name, 0.0)
            obs_dict[f"{joint_name}.vel"] = velocities.get(joint_name, 0.0)

        # Capture camera images with dataset-compatible naming
        for cam_key, cam in self.cameras.items():
            obs_dict[f"images.{cam_key}"] = cam.async_read()

        return obs_dict

    def send_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Send action commands to the robot.
        
        Args:
            action: Dictionary containing motor position commands.
                   Can be in format {"joint_name": value} or {"joint_name.pos": value}
            
        Returns:
            Dictionary of actions that were actually sent.
        """
        # Convert action format to match our internal format
        formatted_action = {}
        
        for key, value in action.items():
            if key.endswith('.pos'):
                # Remove .pos suffix for internal use
                joint_name = key[:-4]  # Remove '.pos'
                formatted_action[joint_name] = value
            else:
                # Direct joint name
                formatted_action[key] = value
        
        # Send goal positions to CAN motors
        self.bus.sync_write("Goal_Position", formatted_action)

        return action

    def calibrate(self) -> None:
        """Calibrate the robot motors."""
        # Perform calibration sequence
        self.bus.calibrate()

    def configure(self) -> None:
        """Configure robot parameters."""
        # Configure CAN actuator parameters
        # This could include setting PID parameters, limits, etc.
        print("Configuring CAN actuators...")
        
        # Get motor info for debugging
        motor_info = self.bus.get_all_motor_info()
        for motor_name, info in motor_info.items():
            print(f"Motor {motor_name}: {info}")