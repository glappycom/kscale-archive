
import pykos
import time

# Note that yaw and roll for hip are flipped
JOINT_NAME_TO_KOS_ID = {
    "right_ankle_pitch": 1,
    "right_knee_pitch": 2,
    "right_hip_pitch": 3,
    "right_hip_yaw": 4,
    "right_hip_roll": 5,
    "left_ankle_pitch": 6,
    "left_knee_pitch": 7,
    "left_hip_pitch": 8,
    "left_hip_yaw": 9,
    "left_hip_roll": 10,
    "right_elbow" : 11,
    "right_shoulder_pitch" : 12,
    "right_shoulder_roll" : 13,
    "left_elbow" : 16,
    "left_shoulder_pitch" : 15,
    "left_shoulder_roll": 14
}

# Usage: kos_position[joint_id] = desired_position - offsets[joint_id]
offsets = {
    1: 19.951171875,    # right_ankle_pitch
    2: -17.314453125,   # right_knee_pitch
    3: -19.951171875,   # right_hip_pitch
    4: -46.93359375,    # right_hip_yaw
    5: 0.263671875,     # right_hip_roll
    6: -16.34765625,    # left_ankle_pitch
    7: 21.357421875,    # left_knee_pitch
    8: 18.10546875,     # left_hip_pitch
    9: 57.65625,        # left_hip_yaw
    10: -4.306640625,   # left_hip_roll
    11: -8.173828125,   # right_elbow
    12: -1.40625,       # right_shoulder_pitch
    13: 32.080078125,   # right_shoulder_roll
    14: -29.794921875,  # left_shoulder_roll
    15: 5.2734375,      # left_shoulder_pitch
    16: 10.107421875    # left_elbow
}

offsets_by_name = {name: offsets[JOINT_NAME_TO_KOS_ID[name]] for name in JOINT_NAME_TO_KOS_ID}

# demo = "10.33.85.6"
demo = "wesley-bot-2"

alias = "demo"

ip_aliases = {
  "demo" : demo,
}

kos = pykos.KOS(ip=ip_aliases[alias])

ac = kos.actuator

# Configure all joints

for id in JOINT_NAME_TO_KOS_ID.values():
    ac.configure_actuator(actuator_id=id, torque_enabled=True)

def go_to_zero():
    commands = [{'actuator_id': id, 'position': -1 * offsets[id]} for id in JOINT_NAME_TO_KOS_ID.values()]
    ac.command_actuators(commands)

def stable_stand():
    commands = [{'actuator_id': id, 'position': -1 * offsets[id]} for id in JOINT_NAME_TO_KOS_ID.values()]
    commands[JOINT_NAME_TO_KOS_ID['right_hip_yaw']] = {'actuator_id': JOINT_NAME_TO_KOS_ID['right_hip_yaw'], 'position': -8 - offsets[4]}
    commands[JOINT_NAME_TO_KOS_ID['left_hip_yaw']] = {'actuator_id': JOINT_NAME_TO_KOS_ID['left_hip_yaw'], 'position': 8 - offsets[9]}
    ac.command_actuators(commands)

def right_leg_up_commands() -> list[dict]:
    return [
        {'actuator_id': JOINT_NAME_TO_KOS_ID['right_hip_yaw'], 'position': -8 - offsets_by_name['right_hip_yaw']},
        {'actuator_id': JOINT_NAME_TO_KOS_ID['right_hip_pitch'], 'position': 5 - offsets_by_name['right_hip_pitch']},
        {'actuator_id': JOINT_NAME_TO_KOS_ID['right_knee_pitch'], 'position': -5 - offsets_by_name['right_knee_pitch']},
        {'actuator_id': JOINT_NAME_TO_KOS_ID['right_ankle_pitch'], 'position': -2 - offsets_by_name['right_ankle_pitch']}
    ]

def right_leg_push_commands() -> list[dict]:
    return [
        {'actuator_id': JOINT_NAME_TO_KOS_ID['right_hip_yaw'], 'position': -8 - offsets_by_name['right_hip_yaw']},
        {'actuator_id': JOINT_NAME_TO_KOS_ID['right_hip_pitch'], 'position': -10 - offsets_by_name['right_hip_pitch']},
        {'actuator_id': JOINT_NAME_TO_KOS_ID['right_knee_pitch'], 'position': 3 - offsets_by_name['right_knee_pitch']},
        {'actuator_id': JOINT_NAME_TO_KOS_ID['right_ankle_pitch'], 'position': 8 - offsets_by_name['right_ankle_pitch']}
    ]

def left_leg_up_commands() -> list[dict]:
    return [
        {'actuator_id': JOINT_NAME_TO_KOS_ID['left_hip_yaw'], 'position': 8 - offsets_by_name['left_hip_yaw']},
        {'actuator_id': JOINT_NAME_TO_KOS_ID['left_hip_pitch'], 'position': -5 - offsets_by_name['left_hip_pitch']},
        {'actuator_id': JOINT_NAME_TO_KOS_ID['left_knee_pitch'], 'position': 5 - offsets_by_name['left_knee_pitch']},
        {'actuator_id': JOINT_NAME_TO_KOS_ID['left_ankle_pitch'], 'position': 2 - offsets_by_name['left_ankle_pitch']}
    ]

def left_leg_push_commands() -> list[dict]:
    return [
        {'actuator_id': JOINT_NAME_TO_KOS_ID['left_hip_yaw'], 'position': 8 - offsets_by_name['left_hip_yaw']},
        {'actuator_id': JOINT_NAME_TO_KOS_ID['left_hip_pitch'], 'position': 10 - offsets_by_name['left_hip_pitch']},
        {'actuator_id': JOINT_NAME_TO_KOS_ID['left_knee_pitch'], 'position': -3 - offsets_by_name['left_knee_pitch']},
        {'actuator_id': JOINT_NAME_TO_KOS_ID['left_ankle_pitch'], 'position': -8 - offsets_by_name['left_ankle_pitch']}
    ]

def test_movement():
    stable_stand()
    breakpoint()
    ac.command_actuators(right_leg_push_commands())
    

def scripted_walk():
    # Basic walking sequence
    # Start from a neutral standing position
    stable_stand()
    time.sleep(1)  # Wait for robot to stabilize
    
    for _ in range(100):
        # lift right leg, push left leg
        ac.command_actuators(right_leg_up_commands() + left_leg_push_commands())
        time.sleep(0.3)
        # push right leg, lift left leg
        ac.command_actuators(right_leg_push_commands() + left_leg_up_commands())
        time.sleep(0.3)
        # brief neutral position between steps
        stable_stand()
        time.sleep(0.2)
    
    # Return to neutral position
    go_to_zero()

def disable_torque():
    for id in JOINT_NAME_TO_KOS_ID.values():
        ac.configure_actuator(actuator_id=id, torque_enabled=False)


# scripted_walk()
# # disable_torque()
# test_movement()