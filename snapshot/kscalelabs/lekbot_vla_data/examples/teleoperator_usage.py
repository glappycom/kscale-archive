"""
Example usage of the Teleop Device integration.

This script demonstrates how to use the teleop device with LeRobot tools.
"""

import sys
import time
from pathlib import Path

# Add the package to Python path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "lerobot_teleoperator_teleop"))

from lerobot_teleoperator_teleop import TeleopConfig, Teleop


def main():
    """Example of using the Teleop Device."""
    
    # Create teleoperator configuration
    config = TeleopConfig(
        port="192.168.1.1",  # Network port or device path
        deadzone=0.1,
        max_speed=1.0,
    )
    
    # Initialize teleoperator
    teleop = Teleop(config)
    
    try:
        # Connect to teleoperator
        print("Connecting to teleoperator...")
        teleop.connect()
        print(f"Teleoperator connected: {teleop.is_connected}")
        
        # Read actions for a few seconds
        print("Reading actions (press Ctrl+C to stop)...")
        for i in range(50):  # Read for ~5 seconds at 10Hz
            try:
                action = teleop.get_action()
                print(f"Action: {action}")
                
                # Send some feedback (example)
                feedback = {
                    "force_feedback": 0.5,
                    "vibration": 0.3,
                }
                teleop.send_feedback(feedback)
                
                time.sleep(0.1)  # 10Hz
                
            except KeyboardInterrupt:
                print("Stopping...")
                break
                
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        # Disconnect teleoperator
        print("Disconnecting teleoperator...")
        teleop.disconnect()
        print("Teleoperator disconnected")


if __name__ == "__main__":
    main()
