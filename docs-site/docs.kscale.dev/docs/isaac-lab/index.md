<!-- preserved from https://docs.kscale.dev/docs/isaac-lab via https://web.archive.org/web/20250213230354id_/https://docs.kscale.dev/docs/isaac-lab -->

# Isaac Lab

Train new locomotion and manipulation policies with K-Scale Bots in Isaac Lab.

# Installation

KLab repository requires installation of [IsaacSim](https://developer.nvidia.com/isaac/sim) and [IsaacLab](https://isaac-sim.github.io/IsaacLab/main/index.html) . Below we provide step by step instructions how to install them on Ubuntu 22.04.

## Prerequisites

Make sure you have Ubuntu 22.04 version of OS:

Bash

```
lsb_release -a
#No LSB modules are available.
#Distributor ID:	Ubuntu
#Description:	Ubuntu 22.04.5 LTS
#Release:	22.04
#Codename:	jammy
```

You can now clone Klab repository:

Bash

```
# Install Git LFS
sudo apt-get update
sudo apt-get install git-lfs
git lfs install # initialize git lfs

# clone the repo
git clone git@github.com:kscalelabs/klab.git

# Pull large files (like USD models)
git lfs pull

# Get Isaaclab as a submodule
git submodule update --init --recursive
```

Create the appropriate python environment using [conda](https://docs.anaconda.com/miniconda/):

bash

```
cd IsaacLab
./isaaclab.sh -c isaaclab # create the conda environment
conda activate isaaclab
pip install isaacsim==4.2.0.2 --extra-index-url https://pypi.nvidia.com
pip install isaacsim-extscache-physics==4.2.0.2 isaacsim-extscache-kit==4.2.0.2 isaacsim-extscache-kit-sdk==4.2.0.2 --extra-index-url https://pypi.nvidia.com
```

You can now test if IsaacSim can launch:

Bash

```
isaacsim
```

Logs can be found at `/home/dpsh/.nvidia-omniverse/`. Once confirmed you can install IsaacLab:

Bash

```
# Install additional packages too
sudo apt install cmake build-essential
# run this in the IsaacLab folder
./isaaclab.sh --install # or "./isaaclab.sh -i"
```

## Verify that IsaacLab was installed properly:

### Option 1: Using the isaaclab.sh executable

Note: this works for both the bundled python and the virtual environment

Bash

```
./isaaclab.sh -p source/standalone/tutorials/00_sim/create_empty.py
```

### Option 2: Using python in your virtual environment

Bash

```
python source/standalone/tutorials/00_sim/create_empty.py
```

## Basic locomotion skills

### Install ZBot extension

Bash

```
cd exts/zbot2
python -m pip install -e .
```

### Run training / playing

#### For zbot2

Bash

```
# run training
${ISAAC_LAB_PATH}/isaaclab.sh -p scripts/rsl_rl/train.py --task Velocity-Rough-Zbot2-v0

# run play
${ISAAC_LAB_PATH}/isaaclab.sh -p scripts/rsl_rl/play.py --task Velocity-Rough-Zbot2-Play-v0
```

#### Play from checkpoint

If you want to play from a checkpoint, here is an example command:

Bash

```
# to load checkpoint from
# klab/logs/rsl_rl/zbot2_rough/2025-01-08_19-33-44/model_200.pt
${ISAAC_LAB_PATH}/isaaclab.sh -p scripts/rsl_rl/play.py   --task Velocity-Rough-Zbot2-Play-v0 \
  --num_envs 1 \
  --resume true \
  --load_run 2025-01-08_19-33-44 \
  --checkpoint model_200.pt
```

#### Saving imu plots

Use `play_imu.py` to save imu plots

Bash

```
# NOTE: turn off termination so that it doesn't stop the moment it falls
# NOTE: The loaded checkpoint has to match the current obs config
# The imu plot and data will be the same length as the video
# imu_type is projected_gravity by default
# example command:
${ISAAC_LAB_PATH}/isaaclab.sh -p scripts/rsl_rl/play_imu.py  \
  --task Velocity-Rough-Zbot2-Play-v0 \
  --num_envs 1 \
  --video \
  --video_length 500 \
  --load_run 2025-01-09_04-50-36 \
  --checkpoint model_0.pt
```

# Adding a new robot from URDF

Instructions in [AddNewRobot.md](https://github.com/kscalelabs/klab/blob/master/AddNewRobot.md)

# Troubleshooting

## Wandb logging

Wandb logging relies on rsl\_rl library's wandb logging, so there are a few things to keep in mind.

You need to set the WANDB\_USERNAME to the project's entity name.

Bash

```
export WANDB_USERNAME=project_entity_name
```

Also, to set the wandb experiment name to the log\_dir folder name, you need to change a file in the rsl\_rl library.

In the `rsl_rl/utils/wandb_utils.py` file, change the wandb.run.name to the last folder in log\_dir path as follows:

Python

```
# Change generated name to project-number format            
wandb.run.name = project + wandb.run.name.split("-")[-1] # <--- After this line

# Change wandb run name to the last folder in log_dir path
wandb.run.name = os.path.basename(log_dir)                     # <--- Add this line
```

## Inotify limit

If you see this in the logs at the start of the Omniverse Launcher:

```
Failed to create an inotify instance. Your system may be at the limit of inotify instances. The limit is listed in `/proc/sys/fs/inotify/max_user_watches` but can be modified. A reboot or logging out and back in may also resolve the issue.
```

Increase the limits via the following commands:

Bash

```
sudo sysctl fs.inotify.max_user_instances=8192
sudo sysctl fs.inotify.max_user_watches=524288
sudo sysctl -p
```

## VSCode Environment

For proper indexing of the isaaclab package, you need to set the PYTHONPATH environment variable for Vscode.

1. Create a .env file in the root of the Vscode workspace with the following content:

Bash

```
PYTHONPATH=/path/to/klab/IsaacLab/source/extensions/omni.isaac.lab:/path/to/klab/IsaacLab/source/extensions/omni.isaac.lab_assets:/path/to/klab/IsaacLab/source/extensions/omni.isaac.lab_tasks
```

2. Create a .vscode/settings.json file with the following content:

JSON

```
{
    "python.envFile": "${workspaceFolder}/.env"
}
```

Updated 8 days ago

---

[Mujoco Playground](/docs/mujoco)[Introduction to KOS](/docs/kos)

* [Table of Contents](#)
* + [Installation](#installation)
  + - [Prerequisites](#prerequisites)
    - [Verify that IsaacLab was installed properly:](#verify-that-isaaclab-was-installed-properly)
    - [Basic locomotion skills](#basic-locomotion-skills)
  + [Adding a new robot from URDF](#adding-a-new-robot-from-urdf)
  + [Troubleshooting](#troubleshooting)
  + - [Wandb logging](#wandb-logging)
    - [Inotify limit](#inotify-limit)
    - [VSCode Environment](#vscode-environment)
