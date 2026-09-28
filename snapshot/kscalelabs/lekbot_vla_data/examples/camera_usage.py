"""
Example usage of the Pi Camera integration.

This script demonstrates how to use the Pi camera with LeRobot tools.
"""

import sys
import cv2
import numpy as np
from pathlib import Path

# Add the package to Python path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "lerobot_camera_pi"))

from lerobot_camera_pi import PiConfig, Pi


def main():
    """Example of using the Pi Camera."""
    
    # Create camera configuration
    config = PiConfig(
        device_id="0",  # Camera device ID
        width=640,
        height=480,
        fps=30,
        depth_enabled=True,
        ir_enabled=False,
    )
    
    # Initialize camera
    camera = Pi(config)
    
    try:
        # Connect to camera
        print("Connecting to camera...")
        camera.connect()
        print(f"Camera connected: {camera.is_connected}")
        
        # Capture and display frames
        print("Capturing frames (press 'q' to quit)...")
        for i in range(100):  # Capture 100 frames
            try:
                # Get observation
                obs = camera.get_observation()
                
                # Display RGB image
                rgb = obs["rgb"]
                print(f"Frame {i}: RGB shape {rgb.shape}")
                
                # Display depth if available
                if "depth" in obs:
                    depth = obs["depth"]
                    print(f"  Depth shape: {depth.shape}")
                
                # Display IR if available
                if "ir" in obs:
                    ir = obs["ir"]
                    print(f"  IR shape: {ir.shape}")
                
                # Simple display using OpenCV
                if rgb is not None:
                    # Convert RGB to BGR for OpenCV display
                    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
                    cv2.imshow("My Custom Camera", bgr)
                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
            except KeyboardInterrupt:
                print("Stopping...")
                break
                
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        # Disconnect camera
        print("Disconnecting camera...")
        camera.disconnect()
        cv2.destroyAllWindows()
        print("Camera disconnected")


if __name__ == "__main__":
    main()
