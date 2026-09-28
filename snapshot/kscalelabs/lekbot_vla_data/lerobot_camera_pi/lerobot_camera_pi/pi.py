"""
Pi Camera implementation.

This module implements the LeRobot Camera interface for the Pi
camera device with depth sensing and IR imaging capabilities.
"""

import cv2
import numpy as np
from typing import Any, Dict, Optional

from lerobot.cameras.camera import Camera

from .config_pi import PiConfig


class Pi(Camera):
    """Pi Camera - A camera with advanced features.
    
    This camera implementation provides:
    - RGB image capture
    - Depth sensing (if enabled)
    - IR imaging (if enabled)
    - Real-time image processing
    """
    
    config_class = PiConfig
    name = "pi"

    def __init__(self, config: PiConfig):
        """Initialize the camera with the given configuration.
        
        Args:
            config: Camera configuration containing device_id, resolution, etc.
        """
        super().__init__(config)
        self.config = config
        
        # Initialize OpenCV capture
        self.cap: Optional[cv2.VideoCapture] = None
        self.depth_cap: Optional[cv2.VideoCapture] = None
        self.ir_cap: Optional[cv2.VideoCapture] = None

    def connect(self) -> None:
        """Connect to the camera hardware."""
        if self.is_connected:
            return
            
        # Initialize main camera
        self.cap = cv2.VideoCapture(int(self.config.device_id))
        if not self.cap.isOpened():
            raise ConnectionError(f"Could not open camera {self.config.device_id}")
        
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.config.fps)
        
        # Initialize depth camera if enabled
        if self.config.depth_enabled:
            # For this example, we'll use a second camera index
            # In practice, this might be a different device or API
            depth_device_id = int(self.config.device_id) + 1
            self.depth_cap = cv2.VideoCapture(depth_device_id)
            if self.depth_cap.isOpened():
                self.depth_cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.width)
                self.depth_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.height)
                self.depth_cap.set(cv2.CAP_PROP_FPS, self.config.fps)
        
        # Initialize IR camera if enabled
        if self.config.ir_enabled:
            # For this example, we'll use a third camera index
            ir_device_id = int(self.config.device_id) + 2
            self.ir_cap = cv2.VideoCapture(ir_device_id)
            if self.ir_cap.isOpened():
                self.ir_cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.width)
                self.ir_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.height)
                self.ir_cap.set(cv2.CAP_PROP_FPS, self.config.fps)

    def disconnect(self) -> None:
        """Disconnect from the camera hardware."""
        if not self.is_connected:
            return
            
        # Release all camera captures
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            
        if self.depth_cap is not None:
            self.depth_cap.release()
            self.depth_cap = None
            
        if self.ir_cap is not None:
            self.ir_cap.release()
            self.ir_cap = None

    @property
    def is_connected(self) -> bool:
        """Check if the camera is connected."""
        return (
            self.cap is not None and 
            self.cap.isOpened()
        )

    def read(self) -> np.ndarray:
        """Read a frame from the camera.
        
        Returns:
            RGB image as numpy array.
            
        Raises:
            ConnectionError: If camera is not connected.
        """
        if not self.is_connected:
            raise ConnectionError(f"{self} is not connected.")
        
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to read frame from camera")
        
        # Convert BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

    def read_depth(self) -> Optional[np.ndarray]:
        """Read a depth frame from the camera.
        
        Returns:
            Depth image as numpy array, or None if depth is not enabled.
        """
        if not self.config.depth_enabled or self.depth_cap is None:
            return None
            
        ret, depth_frame = self.depth_cap.read()
        if not ret:
            return None
            
        return depth_frame

    def read_ir(self) -> Optional[np.ndarray]:
        """Read an IR frame from the camera.
        
        Returns:
            IR image as numpy array, or None if IR is not enabled.
        """
        if not self.config.ir_enabled or self.ir_cap is None:
            return None
            
        ret, ir_frame = self.ir_cap.read()
        if not ret:
            return None
            
        return ir_frame

    def get_observation(self) -> Dict[str, Any]:
        """Get camera observation including all enabled modalities.
        
        Returns:
            Dictionary containing RGB, depth, and IR images as available.
        """
        obs = {}
        
        # Always get RGB image
        obs["rgb"] = self.read()
        
        # Get depth if enabled
        if self.config.depth_enabled:
            depth = self.read_depth()
            if depth is not None:
                obs["depth"] = depth
        
        # Get IR if enabled
        if self.config.ir_enabled:
            ir = self.read_ir()
            if ir is not None:
                obs["ir"] = ir
        
        return obs
