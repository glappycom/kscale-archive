"""
Example usage of the KBot Robot with CAN actuators.

This script demonstrates how to use the KBot robot with CAN-based actuators
using the LeRobot integration.
"""

import sys
import time
from pathlib import Path

# Add the package to Python path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "lerobot_robot_kbot"))

from lerobot_robot_kbot import KBotConfig, KBot


def main():
    """Example of using the KBot Robot with CAN actuators."""
    
    # Create robot configuration for CAN actuators
    config = KBotConfig(
        port="can0",  # CAN interface
        left_arm_ids=[11, 12, 13, 14, 15],  # CAN IDs for left arm
        right_arm_ids=[21, 22, 23, 24, 25],  # CAN IDs for right arm
        left_arm_names=[
            "left_shoulder_pitch",
            "left_shoulder_roll", 
            "left_shoulder_yaw",
            "left_elbow",
            "left_wrist",
        ],
        right_arm_names=[
            "right_shoulder_pitch",
            "right_shoulder_roll",
            "right_shoulder_yaw", 
            "right_elbow",
            "right_wrist",
        ],
        max_scaling=0.5,  # Reduced scaling for safety
    )
    
    # Initialize robot
    robot = KBot(config)
    
    try:
        # Connect to robot
        print("Connecting to KBot robot...")
        robot.connect()
        print(f"Robot connected: {robot.is_connected}")
        
        # Get motor information
        print("\nMotor Information:")
        motor_info = robot.bus.get_all_motor_info()
        for motor_name, info in motor_info.items():
            print(f"  {motor_name}: {info}")
        
        # Get current observation
        print("\nGetting observation...")
        obs = robot.get_observation()
        print(f"Observation keys: {list(obs.keys())}")
        
        # Show joint positions
        joint_positions = {k: v for k, v in obs.items() if k in robot.joint_order}
        print(f"Joint positions: {joint_positions}")
        
        # Send a simple action (move all joints slightly)
        print("\nSending action...")
        action = {}
        for joint_name in robot.joint_order:
            action[joint_name] = 0.1  # Small movement
        
        robot.send_action(action)
        print("Action sent successfully")
        
        # Wait a bit and get another observation
        time.sleep(1.0)
        print("\nGetting updated observation...")
        obs_updated = robot.get_observation()
        joint_positions_updated = {k: v for k, v in obs_updated.items() if k in robot.joint_order}
        print(f"Updated joint positions: {joint_positions_updated}")
        
        # Demonstrate calibration
        print("\nCalibrating robot...")
        robot.calibrate()
        
        # Demonstrate configuration
        print("\nConfiguring robot...")
        robot.configure()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Disconnect robot
        print("\nDisconnecting robot...")
        robot.disconnect()
        print("Robot disconnected")


def test_motor_mapping():
    """Test the motor mapping functionality."""
    print("\n=== Testing Motor Mapping ===")
    
    try:
        from lerobot_robot_kbot.motor_mapping import CANMotorMapper
        
        # Create motor mapper
        mapper = CANMotorMapper()
        
        # Get all joints
        all_joints = mapper.get_all_joints()
        print(f"All joints: {all_joints}")
        
        # Get all CAN IDs
        all_can_ids = mapper.get_all_can_ids()
        print(f"All CAN IDs: {all_can_ids}")
        
        # Test joint validation
        test_joints = ["left_shoulder_pitch", "right_elbow", "unknown_joint"]
        valid_joints, invalid_joints = mapper.validate_joint_names(test_joints)
        print(f"Valid joints: {valid_joints}")
        print(f"Invalid joints: {invalid_joints}")
        
        # Get actuator info for a specific joint
        if valid_joints:
            joint_name = valid_joints[0]
            info = mapper.get_actuator_info(joint_name)
            print(f"Actuator info for {joint_name}: {info}")
        
    except Exception as e:
        print(f"Motor mapping test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("KBot CAN Integration Example")
    print("=" * 40)
    
    # Test motor mapping first
    test_motor_mapping()
    
    # Run main example
    main()
