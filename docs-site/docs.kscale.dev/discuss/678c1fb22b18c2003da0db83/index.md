<!-- preserved from https://docs.kscale.dev/discuss/678c1fb22b18c2003da0db83 via https://web.archive.org/web/20250713171643id_/https://docs.kscale.dev/discuss/678c1fb22b18c2003da0db83 -->

# Discussions

[Ask a Question](/discuss-new)

[Back to All](/discuss)

0

## Actuators failure with Smoke !!

6 months ago by null

Hey, Upon running below code, one of the actuator started smoking and we disconnected power cable right after that

python

```
from pykos import KOS

# Connect to KOS running on localhost at port 50051
client = KOS(ip='192.168.42.1', port=50051)

ACTUATOR_NAME_TO_ID = {
    "left_shoulder_yaw": 11,
    "left_shoulder_pitch": 12,
    "left_elbow_yaw": 13,
    "left_gripper": 14,
    "right_shoulder_yaw": 21,
    "right_shoulder_pitch": 22,
    "right_elbow_yaw": 23,
    "right_gripper": 24,
    "left_hip_yaw": 31,
    "left_hip_roll": 32,
    "left_hip_pitch": 33,
    "left_knee_pitch": 34,
    "left_ankle_pitch": 35,
    "right_hip_yaw": 41,
    "right_hip_roll": 42,
    "right_hip_pitch": 43,
    "right_knee_pitch": 44,
    "right_ankle_pitch": 45
}

ACTUATOR_ID_TO_NAME = {v: k for k, v in ACTUATOR_NAME_TO_ID.items()}

for key in ACTUATOR_NAME_TO_ID:
    id = ACTUATOR_NAME_TO_ID[key]

    response = client.actuator.configure_actuator(
        actuator_id=id,
        kp=32,
        kd=32,
        ki=32,
        max_torque=100.0,
        torque_enabled=True,
        zero_position=True
    )
    if response.success:
        print(f"{key}: {id} Actuator configured successfully.")
                
    else:
        print(f"Failed to configure actuator: {response.error}")

# Command multiple actuators
commands = [ ]

for key in ACTUATOR_NAME_TO_ID:
    id = ACTUATOR_NAME_TO_ID[key]
    commands.append({"actuator_id": id, "position": 90.0})

response = client.actuator.command_actuators(commands)
for result in response.results:
    if result.success:
        print(f"Actuator {result.actuator_id} commanded successfully.")
    else:
        print(f"Failed to command actuator {result.actuator_id}: {result.error}")
```

[todo](/discuss?tag=todo)

Add Comment
