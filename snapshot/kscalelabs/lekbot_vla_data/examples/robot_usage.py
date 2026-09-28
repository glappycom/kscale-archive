"""
Example usage of the KBot Robot integration.

This script demonstrates how to use the KBot robot with LeRobot tools.
"""

import sys
from pathlib import Path

# Add the package to Python path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "lerobot_robot_kbot"))

from lerobot_robot_kbot import KBotConfig, KBot


def main():
    """Example of using the KBot Robot."""
    
    # Create robot configuration
    config = KBotConfig(
        port="/dev/ttyUSB0",  # Adjust to your serial port
        baudrate=115200,
    )
    
    # Initialize robot
    robot = KBot(config)
    
    try:
        # Connect to robot
        print("Connecting to robot...")
        robot.connect()
        print(f"Robot connected: {robot.is_connected}")
        
        # Get current observation
        print("Getting observation...")
        obs = robot.get_observation()
        print(f"Observation keys: {list(obs.keys())}")
        print(f"Joint positions: {[obs[f'joint_{i}.pos'] for i in range(1, 6)]}")
        
        # Send a simple action (move all joints slightly)
        print("Sending action...")
        action = {
            "joint_1.pos": 0.1,
            "joint_2.pos": 0.1,
            "joint_3.pos": 0.1,
            "joint_4.pos": 0.1,
            "joint_5.pos": 0.1,
        }
        robot.send_action(action)
        print("Action sent successfully")
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        # Disconnect robot
        print("Disconnecting robot...")
        robot.disconnect()
        print("Robot disconnected")


if __name__ == "__main__":
    main()
