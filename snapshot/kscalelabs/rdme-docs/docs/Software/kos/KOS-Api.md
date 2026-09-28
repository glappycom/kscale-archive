---
title: Python API
excerpt: 'SEE HERE: https://kscalelabs.github.io/api-docs/'
link:
  new_tab: true
  url: https://kscalelabs.github.io/api-docs/pykos/actuator.html
---
# KOS Services API

The KOS API provides a collection of service clients that enable interaction with various hardware components and system resources. Each service client is specialized for a specific aspect of the robot's functionality.

## Service Overview

### Actuator Service
Control motors, servos, and other actuators with precise positioning, velocity, and torque control.

### IMU Service
Access orientation, acceleration, and angular velocity data from the Inertial Measurement Unit.

### LED Matrix Service
Control LED matrix displays for visual feedback, animations, and text display.

### Sound Service
Play audio, record from microphones, and generate tones for auditory feedback.

### Process Manager Service
Monitor system resources, manage processes, and perform system diagnostics.

### Inference Service
Deploy and run machine learning models for on-device inference.

### Simulation Service
Test robot behaviors in a physics simulation environment before deploying to hardware.

## Using Services

All services follow a consistent access pattern through the main KOS client:

```python
import asyncio
from pykos import KOS

async def main():
    async with KOS() as client:
        # Access a service
        actuator_client = client.actuator()
        imu_client = client.imu()
        
        # Use service methods
        orientation = await imu_client.get_orientation()
        await actuator_client.command_actuators([
            {"actuator_id": 1, "position": orientation.roll + 90.0}
        ])

asyncio.run(main())
```

## Service Documentation

Each service has its own dedicated documentation page with detailed API reference and examples:

- [Actuator Service](./actuator)
- [IMU Service](./imu)
- [LED Matrix Service](./led_matrix)
- [Sound Service](./sound)
- [Process Manager Service](./process_manager)
- [Inference Service](./inference)
- [Simulation Service](./sim)