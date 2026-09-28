---
title: Onshape to URDF Converter
excerpt: K-Scale's toolkit for converting Onshape files to URDFs.
deprecated: false
hidden: false
metadata:
  robots: index
---
See the source code for this repository [here](https://github.com/kscalelabs/onshape) .

# Getting Started

## Dependencies

The `onshape` package requires Python 3.11 or greater.

## Installation

`onshape` can be installed through `pip` using the following command:

```bash
pip install onshape  # To install the vanilla version
pip install 'onshape[all]'  # To install with all dependencies
```

Verify that the package was installed correctly by checking that the `onshape` CLI is available:

```text
$ onshape
usage: onshape {run,download,postprocess,pybullet,mujoco}
onshape: error: the following arguments are required: subcommand
```

Next, you should retrieve an Onshape Access Key and Secret Key from [here](https://cad.onshape.com/appstore/dev-portal) . Set the required environment variables like so:

```
export ONSHAPE_ACCESS_KEY='XXXXXXXXXXXXXXXXXXXXXXXX'
export ONSHAPE_SECRET_KEY='YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
```

# Usage

The Onshape CLI has the following components:

* `download` - takes a link to an Onshape assembly and downloads it as a URDF
* `postprocess` - takes a path to a downloaded URDF and applies postprocessing to make it useful
* `run` - Combines `download` and `postprocess` into a single script
* `pybullet` - Opens a Pybullet visualization of a generated URDF file, for debugging purposes
* `mujoco` - Opens a Mujoco visualization of a generated MJCF file, for debugging purposes

## Download

To download a URDF file, use the following command:

```
$ onshape download --help
usage: onshape [-h] [-o OUTPUT_DIR] [-f CONFIG_PATH] [-n] document_url

positional arguments:
  document_url          The URL of the OnShape document.

options:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        The output directory.
  -f CONFIG_PATH, --config-path CONFIG_PATH
                        The path to the config file.
  -n, --no-cache        Disables caching.
```

You can override configuration options from the command line by passing the values using [omegaconf syntax](https://omegaconf.readthedocs.io/) or by providing a configuration file.

## Postprocess

To postprocess a downloaded URDF file, use the following command:

```
$ onshape postprocess --help
usage: onshape [-h] [-f CONFIG_PATH] urdf_path

positional arguments:
  urdf_path             The path to the downloaded URDF.

options:
  -h, --help            show this help message and exit
  -f CONFIG_PATH, --config-path CONFIG_PATH
                        The path to the config file.
```

You can override the postprocess configuration arguments in the same way.

## Config File Reference

To view all the available configuration options, see [this file](https://github.com/kscalelabs/onshape/blob/master/onshape/onshape/config.py) .

**Ignore Welding Joints**

By default, fixture joints on the same body gets combined into one body. To avoid this you can set the following params:

```yaml
ignore_merging_fixed_joints:
  - "imu_link"
```

or

```yaml
merge_fixed_joints: false
```

**Examples**

<Accordion title="Full Example with Robot" icon="fa-info-circle">
  ```yaml
  default_revolute_joint_effort: 17
  default_revolute_joint_velocity: 360
  suffix_to_joint_effort:
    "_00": 14
    "_02": 17
    "_03": 60
    "_04": 120
  suffix_to_joint_velocity:
    "_00": 12.566
    "_02": 12.566
    "_03": 6.283
    "_04": 6.283
  convex_collision_meshes: true

  ignore_merging_fixed_joints:
    - "imu_link"

  rotate_joints:
    imu_link: [-90.0, 0.0, 0.0]

  max_mesh_triangles: 10000
  max_convex_collision_mesh_triangles: 100

  exclude_collision_meshes:
    # Shoulder yoke stops.
    - "YOKE_STOP_INNER"
    - "YOKE_STOP_INNER_2"
    # Hip yoke stops.
    - "KB_D_102L_L_Hip_Yoke_Drive"
    - "KB_D_102R_R_Hip_Yoke_Drive"
    # Upper arms
    - "L_Bicep_Lower_Drive"
    - "R_Bicep_Lower_Drive"
    # Forearms
    - "L_Forearm_Upper_Drive"
    - "R_Forearm_Upper_Structural"
    # Knee
    - "KB_D_301R_R_Femur_Lower_Drive"
    - "KB_D_301L_L_Femur_Lower_Drive"
    # IMU
    - "imu"

  shrink_collision_meshes:
    # Leg roll
    "RS03_4": 0.8
    "RS03_3": 0.8
    # Ankle
    "KB_D_401R_R_Shin_Drive": 0.85
    "KB_D_402L_L_Shin_Idle": 0.85
    # Wrist
    "KB_C_501X_Bayonet_Adapter_Hard_Stop": 0.8
    "KB_C_501X_Bayonet_Adapter_Hard_Stop_2": 0.8
    # Base
    "KB_B_102B_TORSO_BOTTOM": 0.8

  move_collision_meshes:
    "R_Bicep_Lower_Drive": [0.0, 0.0, -0.01]
    "L_Bicep_Lower_Drive": [0.0, 0.0, -0.01]

  joint_separation_distance: 0.001

  base_rpy:
    - 0
    - 0
    - 4.7123889803 # So that x is forward in mujoco

  flip_joints:
    - "left_knee_04"
    - "left_shoulder_roll_03"
    - "right_shoulder_roll_03"
    - "left_hip_roll_03"
    - "right_hip_roll_03"
    - "left_ankle_02"

  mjcf_metadata:
    joint_params:
      - name: "motor_00"
        armature: 0.0005
        frictionloss: 0.1
        actuatorfrc: 14
        suffixes: ["_00"]
      - name: "motor_02"
        armature: 0.002
        frictionloss: 0.1
        actuatorfrc: 17
        suffixes: ["_02"]
      - name: "motor_03"
        armature: 0.005
        frictionloss: 0.3
        actuatorfrc: 60
        suffixes: ["_03"]
      - name: "motor_04"
        armature: 0.007
        frictionloss: 0.1
        actuatorfrc: 120
        suffixes: ["_04"]

    # imus:
    #   - body_name: "imu"
    #     acc_noise: 0.01
    #     gyro_noise: 0.01
    #     mag_noise: 0.05
  # This is for debugging purposes.
  # use_collision_meshes_as_visual_meshes: true
  ```
</Accordion>

<br />

# CAD Considerations

`onshape` currently only supports`Fixture` mates and `Revolute` joints.

* You must set joint limits for all `Revolute` joints
  * Pay attention to orientation of the axes and the 0-position
  * Onshape provides a dropdown action "reset" on all mates to return to 0-position
* Ensure that there are no redundant mates in your assembly, as they will interfere with generating a sensible graph structure for the URDF

# Tips and Tricks

We suggest first downloading your URDF file using the `download` command, then checking to make sure that it looks correct. Once this works, you can then `postprocess` the resulting URDF to clean up the meshes.

Note that 500 errors or other errors that happen during the initial download phase can sometimes be fixed just by rerunning the command (in our experience, the Onshape API can be a bit flaky).

The Onshape tool includes quite a few checks to make sure that the robot model can be converted to a valid URDF, although sometimes these checks can be overly restrictive to prevent unintended side effects. If you encounter an issue, the error message should be relatively informative - if it is not, please file an issue on our Github page.

# FAQ

How to update permission? After requesting permissions, remove \~/.kscale/

# Additional Resources

## Get Help

* [Github Issues](https://github.com/kscalelabs/onshape/issues)

## OnShape API

* [OnShape API Explorer Glassworks](https://cad.onshape.com/glassworks/explorer/)
* [OnShape API Documentation](https://onshape-public.github.io/docs/api-intro/)

## Other Tools

* [Rhoban's Onshape-to-Robot Github](https://github.com/Rhoban/onshape-to-robot)