<!-- preserved from https://docs.kscale.dev/docs/reference via https://web.archive.org/web/20250213223620id_/https://docs.kscale.dev/docs/reference -->

# PyKOS Reference

pykos is the python interface for KOS (robot operating system)

# KOS Client

Main client class for interacting with KOS

Python

```
from pykos import KOS

# Connect to robot
kos = KOS(ip='192.168.1.100', port=50051)
```

### Parameters

* `ip` (str, optional): IP address of robot. Default: 'localhost'
* `port` (int, optional): Port number. Default: 50051

# IMU Methods

## get\_imu\_values

Get the latest IMU sensor values

Python

```
values = kos.imu.get_imu_values()
```

Returns: `IMUValuesResponse`

## get\_imu\_advanced\_values

Get the latest IMU advanced values

Python

```
values = kos.imu.get_imu_advanced_values()
```

Returns: `IMUAdvancedValuesResponse`

## get\_euler\_angles

Get the latest Euler angles

Python

```
angles = kos.imu.get_euler_angles()
```

Returns: `EulerAnglesResponse`

## get\_quaternion

Get the latest quaternion orientation

Python

```
quat = kos.imu.get_quaternion()
```

Returns: `QuaternionResponse`

## zero

Zero the IMU

Python

```
# Basic zeroing
kos.imu.zero()

# Advanced zeroing
kos.imu.zero(duration=2.0, max_angular_error=0.1)
```

### Parameters

* `duration` (float, optional): Duration in seconds. Default: 1.0
* `max_retries` (int, optional): Maximum number of retries
* `max_angular_error` (float, optional): Maximum angular error during zeroing
* `max_velocity` (float, optional): Maximum velocity during zeroing
* `max_acceleration` (float, optional): Maximum acceleration during zeroing

# Actuator Methods

## calibrate

Calibrate an actuator

Python

```
status = kos.actuator.calibrate(actuator_id=1)
```

### Parameters

* `actuator_id` (int): ID of the actuator to calibrate

Returns: `CalibrationMetadata`

## command\_actuators

Command multiple actuators at once

Python

```
commands = [
    {'actuator_id': 1, 'position': 90},
    {'actuator_id': 2, 'velocity': 10}
]
response = kos.actuator.command_actuators(commands)
```

### Parameters

* `commands` (list): List of actuator commands. Each command is a dict with:
  + `actuator_id` (int): ID of the actuator
  + `position` (float, optional): Target position
  + `velocity` (float, optional): Target velocity
  + `torque` (float, optional): Target torque

# Types

## IMUResponse

Python

```
class IMUResponse:
    acceleration: list[float]      # Acceleration values in m/s^2
    angular_velocity: list[float] # Angular velocity values in rad/s
    orientation: list[float]      # Orientation quaternion
```

## ActuatorResponse

Python

```
class ActuatorResponse:
    position: float  # Current position
    velocity: float  # Current velocity
    torque: float    # Current torque
```

## CalibrationMetadata

Python

```
class CalibrationMetadata:
    status: str     # Current calibration status
    actuator_id: int  # ID of calibrated actuator
```

Updated 21 days ago

---

[Flashing Z-Bot](/docs/flashing-z-bot)[Connecting to Z-Bot](/docs/checking-ip)

* [Table of Contents](#)
* + [KOS Client](#kos-client)
  + [IMU Methods](#imu-methods)
  + - [get\_imu\_values](#get_imu_values)
    - [get\_imu\_advanced\_values](#get_imu_advanced_values)
    - [get\_euler\_angles](#get_euler_angles)
    - [get\_quaternion](#get_quaternion)
    - [zero](#zero)
  + [Actuator Methods](#actuator-methods)
  + - [calibrate](#calibrate)
    - [command\_actuators](#command_actuators)
  + [Types](#types)
  + - [IMUResponse](#imuresponse)
    - [ActuatorResponse](#actuatorresponse)
    - [CalibrationMetadata](#calibrationmetadata)
