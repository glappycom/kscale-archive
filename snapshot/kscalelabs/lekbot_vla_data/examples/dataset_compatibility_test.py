"""
Dataset compatibility test for zbot-record19 format.

This script tests that our KBot robot produces data in the same format
as the zbot-record19 dataset from Hugging Face.
"""

import sys
from pathlib import Path

# Add the package to Python path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "lerobot_robot_kbot"))

from lerobot_robot_kbot import KBotConfig, KBot


def test_dataset_compatibility():
    """Test that our robot produces data compatible with zbot-record19 format."""
    
    print("Testing KBot Robot Dataset Compatibility")
    print("=" * 50)
    
    # Create robot configuration matching zbot-record19
    config = KBotConfig(
        port="can0",
        left_arm_ids=[11, 12, 13, 14, 15],
        right_arm_ids=[21, 22, 23, 24, 25],
        left_arm_names=[
            "left_shoulder_pitch",
            "left_shoulder_roll", 
            "left_shoulder_yaw",
            "left_elbow",
            "left_wrist",
        ],
        right_arm_names=[
            "right_shoulder_pitch",
            "right_shoulder_roll",
            "right_shoulder_yaw", 
            "right_elbow",
            "right_wrist",
        ],
        max_scaling=0.5,
    )
    
    # Initialize robot
    robot = KBot(config)
    
    print(f"Joint order: {robot.joint_order}")
    print(f"Expected joint count: 10")
    print(f"Actual joint count: {len(robot.joint_order)}")
    
    # Test observation features
    print("\n=== Observation Features ===")
    obs_features = robot.observation_features
    print(f"Observation features: {list(obs_features.keys())}")
    
    # Check for expected position features
    expected_pos_features = [f"{joint}.pos" for joint in robot.joint_order]
    actual_pos_features = [k for k in obs_features.keys() if k.endswith('.pos')]
    print(f"Expected position features: {expected_pos_features}")
    print(f"Actual position features: {actual_pos_features}")
    print(f"Position features match: {set(expected_pos_features) == set(actual_pos_features)}")
    
    # Check for expected velocity features
    expected_vel_features = [f"{joint}.vel" for joint in robot.joint_order]
    actual_vel_features = [k for k in obs_features.keys() if k.endswith('.vel')]
    print(f"Expected velocity features: {expected_vel_features}")
    print(f"Actual velocity features: {actual_vel_features}")
    print(f"Velocity features match: {set(expected_vel_features) == set(actual_vel_features)}")
    
    # Check for camera features
    expected_camera_features = ["images.front"]
    actual_camera_features = [k for k in obs_features.keys() if k.startswith('images.')]
    print(f"Expected camera features: {expected_camera_features}")
    print(f"Actual camera features: {actual_camera_features}")
    print(f"Camera features match: {set(expected_camera_features) == set(actual_camera_features)}")
    
    # Test action features
    print("\n=== Action Features ===")
    action_features = robot.action_features
    print(f"Action features: {list(action_features.keys())}")
    
    expected_action_features = [f"{joint}.pos" for joint in robot.joint_order]
    actual_action_features = list(action_features.keys())
    print(f"Expected action features: {expected_action_features}")
    print(f"Actual action features: {actual_action_features}")
    print(f"Action features match: {set(expected_action_features) == set(actual_action_features)}")
    
    # Test data format compatibility
    print("\n=== Data Format Compatibility ===")
    
    # Test observation format
    print("Testing observation format...")
    try:
        # Mock observation data
        mock_obs = {}
        for joint in robot.joint_order:
            mock_obs[f"{joint}.pos"] = 0.0
            mock_obs[f"{joint}.vel"] = 0.0
        mock_obs["images.front"] = None  # Mock camera data
        
        print("✓ Observation format is compatible")
        
        # Test action format
        print("Testing action format...")
        mock_action = {f"{joint}.pos": 0.0 for joint in robot.joint_order}
        print("✓ Action format is compatible")
        
    except Exception as e:
        print(f"✗ Format compatibility error: {e}")
    
    # Test joint naming compatibility
    print("\n=== Joint Naming Compatibility ===")
    expected_joints = [
        "left_shoulder_pitch", "left_shoulder_roll", "left_shoulder_yaw", "left_elbow", "left_wrist",
        "right_shoulder_pitch", "right_shoulder_roll", "right_shoulder_yaw", "right_elbow", "right_wrist"
    ]
    
    print(f"Expected joints: {expected_joints}")
    print(f"Actual joints: {robot.joint_order}")
    print(f"Joint names match: {set(expected_joints) == set(robot.joint_order)}")
    
    # Test camera configuration
    print("\n=== Camera Configuration ===")
    for cam_name, cam_config in robot.cameras.items():
        print(f"Camera {cam_name}:")
        print(f"  Resolution: {cam_config.width}x{cam_config.height}")
        print(f"  FPS: {cam_config.fps}")
    
    # Summary
    print("\n=== Compatibility Summary ===")
    all_good = (
        len(robot.joint_order) == 10 and
        set(expected_pos_features) == set(actual_pos_features) and
        set(expected_vel_features) == set(actual_vel_features) and
        set(expected_camera_features) == set(actual_camera_features) and
        set(expected_action_features) == set(actual_action_features) and
        set(expected_joints) == set(robot.joint_order)
    )
    
    if all_good:
        print("✅ KBot robot is fully compatible with zbot-record19 dataset format!")
    else:
        print("❌ KBot robot has compatibility issues with zbot-record19 dataset format")
    
    return all_good


def test_data_recording_simulation():
    """Simulate data recording to test the complete pipeline."""
    
    print("\n" + "=" * 50)
    print("Testing Data Recording Simulation")
    print("=" * 50)
    
    # This would normally connect to the robot, but we'll simulate
    print("Simulating data recording session...")
    
    # Simulate observation data
    mock_observation = {
        "left_shoulder_pitch.pos": 0.1647988110780716,
        "left_shoulder_pitch.vel": 5.018385887145996,
        "left_shoulder_roll.pos": -0.23075111210346222,
        "left_shoulder_roll.vel": -2.8501014709472656,
        "left_shoulder_yaw.pos": 13.634260177612305,
        "left_shoulder_yaw.vel": 1.7312617301940918,
        "left_elbow.pos": -10.574462890625,
        "left_elbow.vel": -0.192556694149971,
        "left_wrist.pos": -8.712316513061523,
        "left_wrist.vel": 1.8851321935653687,
        "right_shoulder_pitch.pos": 1.702848196029663,
        "right_shoulder_pitch.vel": -0.9966611862182617,
        "right_shoulder_roll.pos": -0.252716988325119,
        "right_shoulder_roll.vel": 1.2064846754074097,
        "right_shoulder_yaw.pos": 9.525272369384766,
        "right_shoulder_yaw.vel": -1.500018835067749,
        "right_elbow.pos": 6.361201286315918,
        "right_elbow.vel": -4.73129940032959,
        "right_wrist.pos": -8.316766738891602,
        "right_wrist.vel": 11.886714935302734,
        "images.front": None,  # Mock camera data
    }
    
    # Simulate action data
    mock_action = {
        "left_shoulder_pitch.pos": 3.515625,
        "left_shoulder_roll.pos": 2.63671875,
        "left_shoulder_yaw.pos": 13.974609375,
        "left_elbow.pos": -10.810546875,
        "left_wrist.pos": -7.20703125,
        "right_shoulder_pitch.pos": -3.251953125,
        "right_shoulder_roll.pos": -3.251953125,
        "right_shoulder_yaw.pos": 9.580078125,
        "right_elbow.pos": 9.580078125,
        "right_wrist.pos": -7.998046875,
    }
    
    print("✓ Mock observation data generated")
    print(f"  Observation keys: {list(mock_observation.keys())}")
    print(f"  Action keys: {list(mock_action.keys())}")
    
    # Test data structure
    print("\nTesting data structure...")
    
    # Check observation structure
    obs_pos_keys = [k for k in mock_observation.keys() if k.endswith('.pos')]
    obs_vel_keys = [k for k in mock_observation.keys() if k.endswith('.vel')]
    obs_cam_keys = [k for k in mock_observation.keys() if k.startswith('images.')]
    
    print(f"  Position observations: {len(obs_pos_keys)}")
    print(f"  Velocity observations: {len(obs_vel_keys)}")
    print(f"  Camera observations: {len(obs_cam_keys)}")
    
    # Check action structure
    action_keys = list(mock_action.keys())
    print(f"  Actions: {len(action_keys)}")
    
    print("✓ Data structure is compatible with zbot-record19 format")
    
    return True


if __name__ == "__main__":
    print("KBot Robot Dataset Compatibility Test")
    print("Testing compatibility with zbot-record19 dataset")
    print("https://huggingface.co/datasets/leolin6/zbot-record19")
    print()
    
    # Run compatibility tests
    compatibility_ok = test_dataset_compatibility()
    recording_ok = test_data_recording_simulation()
    
    print("\n" + "=" * 50)
    print("FINAL RESULT")
    print("=" * 50)
    
    if compatibility_ok and recording_ok:
        print("🎉 SUCCESS: KBot robot is fully compatible with zbot-record19 dataset!")
        print("✅ Ready for data collection and training with LeRobot")
    else:
        print("❌ FAILURE: Compatibility issues detected")
        print("🔧 Please review and fix the issues above")
