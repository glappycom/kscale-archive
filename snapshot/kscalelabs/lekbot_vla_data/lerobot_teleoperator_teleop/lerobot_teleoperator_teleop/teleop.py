"""
Teleop Device implementation.

This module implements the LeRobot Teleoperator interface for a
teleoperation device using gamepad/joystick input.
"""

import pygame
from typing import Any, Dict

from lerobot.teleoperators.teleoperator import Teleoperator

from .config_teleop import TeleopConfig


class Teleop(Teleoperator):
    """Teleop Device - A teleoperation device.
    
    This teleoperator implementation provides:
    - Gamepad/joystick input handling
    - Action generation for robot control
    - Feedback mechanisms
    - Real-time control interface
    """
    
    config_class = TeleopConfig
    name = "teleop"

    def __init__(self, config: TeleopConfig):
        """Initialize the teleoperator with the given configuration.
        
        Args:
            config: Teleoperator configuration containing port, deadzone, etc.
        """
        super().__init__(config)
        self.config = config
        
        # Initialize pygame for joystick support
        pygame.init()
        pygame.joystick.init()
        
        # Initialize joystick if available
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

    @property
    def action_features(self) -> Dict[str, Any]:
        """Define the structure of action commands from the teleoperator.
        
        Returns:
            Dictionary describing action features for robot control.
        """
        return {
            "joint_1.pos": float,
            "joint_2.pos": float,
            "joint_3.pos": float,
            "joint_4.pos": float,
            "joint_5.pos": float,
        }

    @property
    def feedback_features(self) -> Dict[str, Any]:
        """Define the structure of feedback that can be sent to the teleoperator.
        
        Returns:
            Dictionary describing feedback features.
        """
        return {
            "force_feedback": float,
            "vibration": float,
        }

    def connect(self) -> None:
        """Connect to the teleoperator hardware."""
        if self.is_connected:
            return
            
        # Initialize joystick connection
        if self.joystick is None and pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

    def disconnect(self) -> None:
        """Disconnect from the teleoperator hardware."""
        if not self.is_connected:
            return
            
        # Disconnect joystick
        if self.joystick is not None:
            self.joystick.quit()
            self.joystick = None

    @property
    def is_connected(self) -> bool:
        """Check if the teleoperator is connected."""
        return self.joystick is not None and self.joystick.get_init()

    def get_action(self) -> Dict[str, Any]:
        """Get action commands from the teleoperator.
        
        Returns:
            Dictionary containing action commands for robot control.
            
        Raises:
            ConnectionError: If teleoperator is not connected.
        """
        if not self.is_connected:
            raise ConnectionError(f"{self} is not connected.")

        # Process pygame events
        pygame.event.pump()
        
        # Read joystick axes and apply deadzone
        axes = []
        for i in range(min(5, self.joystick.get_numaxes())):
            axis_value = self.joystick.get_axis(i)
            # Apply deadzone
            if abs(axis_value) < self.config.deadzone:
                axis_value = 0.0
            # Scale by max_speed
            axis_value *= self.config.max_speed
            axes.append(axis_value)
        
        # Pad with zeros if we don't have enough axes
        while len(axes) < 5:
            axes.append(0.0)

        return {
            "joint_1.pos": axes[0],
            "joint_2.pos": axes[1],
            "joint_3.pos": axes[2],
            "joint_4.pos": axes[3],
            "joint_5.pos": axes[4],
        }

    def send_feedback(self, feedback: Dict[str, Any]) -> None:
        """Send feedback to the teleoperator.
        
        Args:
            feedback: Dictionary containing feedback data.
        """
        if not self.is_connected:
            return
            
        # Example feedback implementation
        # This could control force feedback, vibration, LEDs, etc.
        force_feedback = feedback.get("force_feedback", 0.0)
        vibration = feedback.get("vibration", 0.0)
        
        # Apply feedback to the device
        # Note: This is a placeholder - actual implementation depends on hardware
        if hasattr(self.joystick, 'rumble'):
            # Use rumble if available
            self.joystick.rumble(force_feedback, vibration, 100)
