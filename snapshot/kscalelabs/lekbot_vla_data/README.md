# LeRobot Hardware Integration Repository

This repository contains Python packages for integrating custom hardware with the LeRobot ecosystem. Each package follows the LeRobot plugin conventions for automatic discovery.

## Repository Structure

```
lerobot-hardware-integration/
├── README.md
├── pyproject.toml                    # Root workspace configuration
├── requirements.txt                  # Common dependencies
├── lerobot_robot_kbot/              # KBot robot integration package
├── lerobot_teleoperator_teleop/     # Teleop device integration package
├── lerobot_camera_pi/               # Pi camera integration package
└── examples/                        # Usage examples
```

## Package Naming Conventions

LeRobot automatically discovers packages with these prefixes:
- `lerobot_robot_*` - for robot integrations
- `lerobot_teleoperator_*` - for teleoperation devices  
- `lerobot_camera_*` - for camera integrations

## Installation

### Development Installation
```bash
# Install all packages in development mode
pip install -e ./lerobot_robot_kbot
pip install -e ./lerobot_teleoperator_teleop
pip install -e ./lerobot_camera_pi
```

### Production Installation
```bash
# Install from PyPI (when published)
pip install lerobot-robot-kbot
pip install lerobot-teleoperator-teleop
pip install lerobot-camera-pi
```

## Usage

Once installed, LeRobot will automatically discover your hardware integrations:

```bash
# Use your KBot robot
lerobot-teleoperate --robot.type=kbot --robot.port=/dev/ttyUSB0

# Use your teleop device  
lerobot-teleoperate --teleop.type=teleop

# Use your Pi camera
lerobot-record --camera.type=pi
```

## Development

Each package follows the LeRobot plugin conventions:

1. **Naming**: Package names must start with the appropriate prefix
2. **Structure**: Config and device classes follow `SomethingConfig`/`Something` pattern
3. **Discovery**: Classes are exposed in `__init__.py`
4. **Dependencies**: Each package lists `lerobot` as a dependency

## Examples

See the `examples/` directory for complete integration examples and usage patterns.

### CAN Integration

The KBot robot package includes integration with CAN-based actuators using the pyfirmware system:

```python
from lerobot_robot_kbot import KBotConfig, KBot

# Configure for CAN actuators
config = KBotConfig(
    port="can0",
    left_arm_ids=[11, 12, 13, 14, 15],
    right_arm_ids=[21, 22, 23, 24, 25],
    max_scaling=0.5,
)

# Initialize robot
robot = KBot(config)
robot.connect()

# Use with LeRobot tools
obs = robot.get_observation()
robot.send_action({"left_shoulder_pitch": 0.1})
```

See `examples/kbot_can_usage.py` for a complete example.

### Dataset Compatibility

The KBot robot is fully compatible with the [zbot-record19 dataset](https://huggingface.co/datasets/leolin6/zbot-record19) format:

- **10 joint actions**: `left_shoulder_pitch.pos`, `left_shoulder_roll.pos`, etc.
- **20 joint observations**: Position and velocity for each joint
- **Camera support**: `images.front` (240x320x3 at 60 FPS)
- **Dual-arm configuration**: Left and right arm control

```python
# Test dataset compatibility
python examples/dataset_compatibility_test.py
```

This ensures seamless integration with existing LeRobot datasets and training pipelines.

## Setup Guide

For detailed setup instructions, including handling Python version conflicts and different motor interfaces, see [SETUP_GUIDE.md](SETUP_GUIDE.md).

### Quick Start

```bash
# Install LeRobot
pip install lerobot

# Install KBot robot package
pip install -e ./lerobot_robot_kbot

# Test with simulated motors (no hardware required)
python examples/dataset_compatibility_test.py
```
