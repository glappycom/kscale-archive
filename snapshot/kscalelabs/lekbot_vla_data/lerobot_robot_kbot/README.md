# LeRobot Robot Integration: KBot

This package provides LeRobot integration for the KBot robot arm using Feetech servos.

## Features

- 5-DoF robot arm control
- Feetech servo integration
- Camera support
- Calibration and configuration
- Real-time position control

## Installation

```bash
pip install -e ./lerobot_robot_my_robot
```

## Usage

Once installed, you can use this robot with LeRobot tools:

```bash
# Teleoperate the robot
lerobot-teleoperate --robot.type=kbot --robot.port=/dev/ttyUSB0

# Record data
lerobot-record --robot.type=kbot --robot.port=/dev/ttyUSB0

# Train policies
lerobot-train --policy.type=act --robot.type=kbot
```

## Configuration

The robot supports the following configuration options:

- `port`: Serial port for Feetech servo communication
- `cameras`: Camera configuration dictionary
- `baudrate`: Communication baudrate (default: 115200)

## Hardware Requirements

- 5x Feetech STS/SMS series servos
- USB-to-Serial adapter
- Optional: USB camera for visual feedback
