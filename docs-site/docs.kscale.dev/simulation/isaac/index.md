<!-- preserved from https://docs.kscale.dev/simulation/isaac via https://web.archive.org/web/20241111162907id_/https://docs.kscale.dev/simulation/isaac -->

# Isaac Gym - K-Scale Docs

[Simulation](/simulation/mujoco "Simulation")Isaac Gym

# Isaac Gym

A library for simulating Stompy in Isaac Gym.

[Github](https://github.com/kscalelabs/sim)

This library is built on top of the Isaac Gym library and Humanoid-gym and provides a simple interface for running experiments with Stompy. We have defined the following tasks:

* Getting up
* Walking

We currently support Stompy Mini, XBot, Unitree G1 and H1 with more humanoids to come.

The walking task works reliably with the upper body fixed. The getting up task is still an open challenge!

## Getting Started

This repository requires Python 3.8 due to compatibility issues with underlying libraries. We hope to support more recent Python versions in the future.

1. Clone this repository:

```
git clone https://github.com/kscalelabs/sim.git
cd sim
```

2. Create a new conda environment and install the package:

```
conda create --name kscale-sim-library python=3.8.19
conda activate kscale-sim-library
make install-dev
```

3. Install third-party dependencies:

Manually download `IsaacGym_Preview_4_Package.tar.gz` from <https://developer.nvidia.com/isaac-gym>, and run:

```
tar -xvf IsaacGym_Preview_4_Package.tar.gz
conda env config vars set ISAACGYM_PATH=`pwd`/isaacgym
conda deactivate
conda activate kscale-sim-library
make install-third-party-external
```

## Running Stompy experiments

1. Pre-define model directory:

```
export MODEL_DIR=sim/resources/stompymini
```

2. Run a small training with visualization with the following command:

```
python sim/train.py --task=stompymini --num_envs=4
```

or full training in the headless mode:

```
python sim/train.py --task=stompymini --num_envs=4096 --headless
```

3. Run evaluation with the following command:

```
python sim/play.py --task stompymini --sim_device cpu
```

See [this doc](https://docs.google.com/document/d/1YZzBqIXO7oq7vIKu-BZr5ssNsi3nKtxpRPnfSnTXojA/edit?usp=sharing) for more beginner tips.

## Adding a new robot

Creating a new embodiment is quite straightforward. The best way is to copy an existing robot and modify it.

The best starting point would be [stompymini](https://github.com/kscalelabs/sim/tree/master/sim/resources/stompymini).

1. Create a folder with a new robot [here](https://github.com/kscalelabs/sim/tree/master/sim/resources).
2. Add `joint.py` file setting up basic properties and joint configuration - see an [example](https://github.com/kscalelabs/sim/blob/master/sim/resources/stompymini/joints.py).
   * Make sure to update the p\_gains (def stiffness) and d\_gains (def damping), such that the joints match the URDF joint names.
3. Update [height](https://github.com/kscalelabs/sim/blob/aa97ddfddcaadcac64d4f83d986548cc7fc451a6/sim/resources/stompymini/joints.py#L102) and default rotation of your humanoid.
4. Add a new embodiment configuration and environment [here](https://github.com/kscalelabs/sim/tree/master/sim/envs/humanoids).
5. Add a new embodiment to the [registry](https://github.com/kscalelabs/sim/blob/master/sim/envs/__init__.py).
   To run things export your default path:

```
export MODEL_DIR=sim/resources/NEW_HUMANOID
```

and kick off the training:

```
python sim/train.py --env-id NEW_HUMANOID --num-envs 4
```

## Making it stand

1. The best way to start is to make your new robot stand. In this case you want to comment out the rewards that are responsible for making the robot walk. See an example of a [reward config](https://github.com/kscalelabs/sim/blob/aa97ddfddcaadcac64d4f83d986548cc7fc451a6/sim/envs/humanoids/stompymini_config.py#L163).
2. If the robot flies away, inspect your joint limits. During training, we introduce a lot of noise to the default joint positions as well as masses. You might need either adapt the limits or the [noise level](https://github.com/kscalelabs/sim/blob/aa97ddfddcaadcac64d4f83d986548cc7fc451a6/sim/envs/humanoids/stompy_config.py#L213).
3. Isaac Sim often hits velocities nans when some joints are hitting their limits - you can change the [engine parameters](https://github.com/kscalelabs/sim/blob/aa97ddfddcaadcac64d4f83d986548cc7fc451a6/sim/envs/humanoids/stompy_config.py#L108) to fix this issue.
4. The revolute joints cannot have 0 velocity in the URDF definition - otherwise, engine will go nans as well.
5. Observe the reward for orientation and default joint position. The model should just farm these two rewards.
6. If the robot still struggles at keeping the standing pose, you can also change the urdf definition using the [script](https://github.com/kscalelabs/sim/blob/master/sim/scripts/create_fixed_torso.py) to fix the upper body or change joint limits.

## Making it walk

We set up the logic so that your new robot should start to walk with basic configuration after some modifications.

1. To get things going it’s best to start from the good standing pose, with knees slightly bent. See an example [Stompy’s pose](https://github.com/kscalelabs/sim/blob/aa97ddfddcaadcac64d4f83d986548cc7fc451a6/sim/resources/stompymini/joints.py#L113).
2. The [gait reward](https://github.com/kscalelabs/sim/blob/aa97ddfddcaadcac64d4f83d986548cc7fc451a6/sim/envs/humanoids/stompy_config.py#L146) is the most crucial single reward. You have to adapt the hyperparameters to your robot design to get it to work.
3. If the robots tends to jump, use only one limb you will have to adapt the overall rewards schema to enforce proper behavior.
4. If the setup is correct, you should see positive results after first 200-300 epochs. However, the robust policy will requires 2000-3000 epochs.

## Common Issues

After cloning Isaac Gym, sometimes the bindings mysteriously disappear.

To fix this, update the submodule:

```
git submodule update --init --recursive
```

If you observe errors with libpython3.8.so.1.0, you can try the following:

```
export LD_LIBRARY_PATH=PATH_TO_YOUR_ENV/lib:$LD_LIBRARY_PATH
```

If you still see segmentation faults, you can try the following:

```
sudo apt-get vulkan1
```

## FAQ

**Frequently Seen Bugs and Errors**

1. *Onshape*
   * Only revolute and fastened joints
   * Set weights or material
   * Add joint limits in Onshape
2. Remove Base to Body Fixed Joint and the Base link. The K-Scale Onshape to URDF converter includes these but they were removed in the Stompy Mini URDF.
3. Flying Robot (walking then flying away like there is a strong gust)
   * Check effort and velocity in limits. For small servos around effort=“24” velocity=“30”, For large humanoids like stompy mini, effort=“80” and velocity=“5”
   * Check `def stiffness` and `def damping`. For stiffness servos should be ~20 for smaller robots using servos, ~150 for larger humanoids. For damping, should be ~0.5 for servo robots and ~10 for larger humanoids using actuators.

### Expected Behavior

These are subject to how you change some of the training params, but generally using the repo mostly as is

1. Episode Length should be >2k
2. Mean reward ~40 for quadruped.
3. Mean reward ~[ ] for humanoid

[Mujoco](/simulation/mujoco "Mujoco")[MinPPO](/simulation/minppo "MinPPO")
