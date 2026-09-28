# KBot Robot Setup Guide

This guide explains how to set up the KBot robot with different motor interfaces, depending on your hardware and Python environment.

## Motor Interface Options

The KBot robot supports multiple motor interfaces to handle different hardware setups and Python version requirements:

### 1. CAN Motors (with pyfirmware) - **Recommended for CAN hardware**

**Requirements:**
- Python 3.8+ (compatible with pyfirmware)
- pyfirmware installed
- CAN hardware (your custom actuators)

**Setup:**
```bash
# Install pyfirmware in the same environment as LeRobot
pip install -e /path/to/pyfirmware

# Install LeRobot
pip install lerobot

# Install KBot robot package
pip install -e ./lerobot_robot_kbot
```

**Usage:**
```python
from lerobot_robot_kbot import KBotConfig, KBot

config = KBotConfig(
    port="can0",  # CAN interface
    left_arm_ids=[11, 12, 13, 14, 15],
    right_arm_ids=[21, 22, 23, 24, 25],
    # ... other config
)

robot = KBot(config)
```

### 2. Simulated Motors - **For testing without hardware**

**Requirements:**
- Any Python version
- No hardware required

**Usage:**
```python
from lerobot_robot_kbot import KBotConfig, KBot

config = KBotConfig(
    port="sim://test",  # Simulated interface
    # ... other config
)

robot = KBot(config)
```

### 3. Serial Motors - **For simple serial-based hardware**

**Requirements:**
- pyserial: `pip install pyserial`
- Serial-based motor controller

**Usage:**
```python
from lerobot_robot_kbot import KBotConfig, KBot

config = KBotConfig(
    port="/dev/ttyUSB0",  # Serial port
    # ... other config
)

robot = KBot(config)
```

## Python Environment Management

### Option 1: Single Environment (Recommended)

If you can make pyfirmware compatible with LeRobot's Python version:

```bash
# Create a new environment
conda create -n lerobot-kbot python=3.10
conda activate lerobot-kbot

# Install LeRobot
pip install lerobot

# Install pyfirmware
pip install -e /path/to/pyfirmware

# Install KBot robot package
pip install -e ./lerobot_robot_kbot
```

### Option 2: Separate Environments

If you need different Python versions:

```bash
# Environment 1: For LeRobot
conda create -n lerobot python=3.11
conda activate lerobot
pip install lerobot
pip install -e ./lerobot_robot_kbot

# Environment 2: For pyfirmware
conda create -n pyfirmware python=3.8
conda activate pyfirmware
pip install -e /path/to/pyfirmware
```

### Option 3: Use Alternative Interfaces

If pyfirmware is not compatible, use simulated or serial interfaces:

```bash
# Install LeRobot
pip install lerobot

# Install KBot robot package (will use alternative interfaces)
pip install -e ./lerobot_robot_kbot

# For serial interface, also install:
pip install pyserial
```

## Configuration Examples

### CAN Configuration (with pyfirmware)
```python
config = KBotConfig(
    port="can0",
    left_arm_ids=[11, 12, 13, 14, 15],
    right_arm_ids=[21, 22, 23, 24, 25],
    max_scaling=0.5,
)
```

### Simulated Configuration (for testing)
```python
config = KBotConfig(
    port="sim://test",
    left_arm_ids=[11, 12, 13, 14, 15],
    right_arm_ids=[21, 22, 23, 24, 25],
    max_scaling=0.5,
)
```

### Serial Configuration (for simple hardware)
```python
config = KBotConfig(
    port="/dev/ttyUSB0",
    left_arm_ids=[11, 12, 13, 14, 15],
    right_arm_ids=[21, 22, 23, 24, 25],
    max_scaling=0.5,
)
```

## Troubleshooting

### Import Error: "firmware not available"

This means pyfirmware is not installed or not compatible. Solutions:

1. **Install pyfirmware:**
   ```bash
   pip install -e /path/to/pyfirmware
   ```

2. **Use alternative interface:**
   ```python
   # Change port to use simulated or serial interface
   config = KBotConfig(port="sim://test")  # or "/dev/ttyUSB0"
   ```

### Python Version Conflicts

If you have Python version conflicts:

1. **Use conda environments** (recommended)
2. **Use alternative interfaces** (simulated/serial)
3. **Modify pyfirmware** to be compatible with your Python version

### Hardware Connection Issues

1. **Check CAN interface:**
   ```bash
   ip link show can0
   ```

2. **Check serial port:**
   ```bash
   ls /dev/ttyUSB*
   ```

3. **Use simulated interface for testing:**
   ```python
   config = KBotConfig(port="sim://test")
   ```

## Testing Your Setup

Run the compatibility test to verify your setup:

```bash
python examples/dataset_compatibility_test.py
```

This will test:
- ✅ Motor interface availability
- ✅ Dataset format compatibility
- ✅ Joint configuration
- ✅ Camera setup

## Next Steps

Once your setup is working:

1. **Test with simulated motors:**
   ```python
   python examples/kbot_can_usage.py
   ```

2. **Record data:**
   ```bash
   lerobot-record --robot.type=kbot_parallel --robot.port=sim://test
   ```

3. **Train policies:**
   ```bash
   lerobot-train --policy.type=act --robot.type=kbot_parallel
   ```

## Support

If you encounter issues:

1. Check the error messages - they provide specific guidance
2. Try the simulated interface first to verify the setup
3. Check that all dependencies are installed correctly
4. Verify your hardware connections
