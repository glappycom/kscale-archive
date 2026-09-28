---
title: Environment
excerpt: >-
  Overview of how different robots, observations and commands are specified in
  K-Sim
deprecated: false
hidden: false
metadata:
  robots: index
---
# Environment Classes

The [Defining a Task](./task.md) section explains how to define your task's environment by implementing abstract methods. These methods return a collection of observations, commands, rewards, terminations, event, and curriculum builders. Each form an aspect of the underlying partially observable Markov decision process (POMDP) that is inherent to your environment. This guide will walk you through standard observations, rewards, terminations, etc. as well as explain how to implement custom environment classes.

## Observations

Observations define the information the agent receives from the environment at each timestep. In KSim, an **observation** is a self-contained class that pulls data from the simulator state, optionally adds noise, and returns a JAX array. These arrays are then concatenated and fed into your policy.

Each observation must subclass `Observation` and implement the following method:

```python
def observe(
    self,
    state: ObservationInput,
    curriculum_level: jax.Array,
    rng: jax.random.PRNGKeyArray,
) -> jax.Array:
    ...
```

* `state`: A wrapper (`ObservationInput`) containing the `PhysicsState`, commands, and internal observation carry state.
* `curriculum_level`: A scalar float (in \[0, 1]) that you can use to scale noise or complexity.
* `rng`: A JAX random key to sample noise, if needed.

Observations can optionally maintain internal **state** (e.g., for smoothing sensors) by subclassing `StatefulObservation`, which requires two additional methods:

```python
def initial_carry(self, rng: PRNGKeyArray) -> PyTree:
    ...

def observe_stateful(
    self,
    state: ObservationInput,
    curriculum_level: Array,
    rng: PRNGKeyArray,
) -> tuple[Array, PyTree]:
    ...
```

***

To define your own observation:

```python
@attrs.define(frozen=True, kw_only=True)
class MyCustomObservation(ksim.Observation):
    def observe(self, state: ksim.ObservationInput, curriculum_level: jax.Array, rng: jax.random.PRNGKeyArray) -> jax.Array:
        # For example, return the base body's X position
        return state.physics_state.data.qpos[0:1]
```

To include it in your task:

```python
def get_observations(self, physics_model: ksim.PhysicsModel) -> list[ksim.Observation]:
    return [
        MyCustomObservation(),
        ...
    ]
```

All observations can inject noise:

```python
MyCustomObservation(noise=0.1, noise_type="gaussian")
```

***

### Example Observations

Below are common observations used in locomotion tasks:

* `JointPositionObservation()`: Joint angles (excluding the free joint).
* `JointVelocityObservation()`: Joint angular velocities.
* `ActuatorForceObservation()`: Current torques being applied at each actuator.
* `ActuatorAccelerationObservation()`: Angular accelerations of joints.
* `BasePositionObservation()`: 3D position of the base body.
* `BaseOrientationObservation()`: Orientation of the base as a quaternion.
* `BaseLinearVelocityObservation()`: World-frame linear velocity of the base.
* `BaseAngularVelocityObservation()`: World-frame angular velocity of the base.
* `BaseLinearAccelerationObservation()`: Linear acceleration of the base.
* `BaseAngularAccelerationObservation()`: Angular acceleration of the base.
* `CenterOfMassInertiaObservation()`: Inertial properties of all non-world bodies.
* `CenterOfMassVelocityObservation()`: Velocities of all non-world bodies.
* `ProjectedGravityObservation.create(...)`: Gravity vector rotated into local frame using quaternion orientation.
* `SensorObservation.create(sensor_name="imu_acc", ...)`: Raw sensor reading (e.g., IMU, contact sensor).
* `SensorObservation.create(sensor_name="forwardvector", ...)`: Orientation vector aligned with robot’s facing direction.
* `FeetContactObservation.create(...)`: Binary contact status for each foot.
* `FeetPositionObservation.create(...)`: Global 3D position of each foot.
* `FeetOrientationObservation.create(...)`: Quaternion orientation of each foot.
* `TimestepObservation()`: Current simulation time as a scalar.
* `ActPosObservation.create(joint_name="hip_joint")`: Returns both commanded and actual joint position (for diagnostics).
* `ActVelObservation.create(joint_name="knee_joint")`: Returns both commanded and actual joint velocity.

Each observation returns a named entry in the environment’s observation dictionary. You can concatenate these arrays manually (as in the walking example) or use them in a structured model.

***

## Commands

Commands provide external high-level input to the agent during training—think of them as the “intent” or goal (e.g. "walk forward", "go to this position", etc.). KSim supports both discrete and continuous commands, and all commands subclass the base `Command` class.

To implement a command, you must define:

```python
def initial_command(
    self,
    physics_data: PhysicsData,
    curriculum_level: jax.Array,
    rng: jax.random.PRNGKeyArray,
) -> jax.Array:
    ...
    
def __call__(
    self,
    prev_command: jax.Array,
    physics_data: PhysicsData,
    curriculum_level: jax.Array,
    rng: jax.random.PRNGKeyArray,
) -> jax.Array:
    ...
```

These methods define how the command is initialized at the start of an episode and how it evolves over time (e.g. changing every few seconds).

***

### Example Commands

* `JoystickCommand()`: Discrete "joystick" intent signal (e.g., 0 = stop, 1 = walk forward, etc.)

* `FloatVectorCommand(ranges=((−1, 1), (−1, 1)))`: Continuous goal vector sampled from a box.

* `IntVectorCommand(ranges=((0, 4),))`: Discrete integer command vector with resampling probability.

* `PositionCommand.create(...)`: Smooth target positions with curriculum-scaled noise and visibility markers for debugging.

All commands automatically support:

* **Stochastic switching** (`switch_prob`)

* **Curriculum-based scaling**

* **Visualization markers** for debugging command intent

During rollout, commands are stored in a dictionary keyed by `command_name`. The policy can access them via `commands["joystick_command"]`, etc.

***

## Terminations

Terminations end an episode early based on some condition (e.g., falling over, hitting the ground, or going out of bounds). Every termination condition must subclass `Termination` and implement:

```python
def __call__(self, state: PhysicsData, curriculum_level: jax.Array) -> jax.Array:
    ...
```

This function returns a value per environment:

* `-1`: failure (negative outcome)

* `1`: success (positive outcome)

* `0`: continue episode

***

### Example Terminations

* `BadZTermination(unhealthy_z_lower=0.9, unhealthy_z_upper=1.6)`: Ends the episode if the robot is too low or too high.

* `PitchTooGreatTermination(max_pitch=π/3)`: Ends the episode if the pitch exceeds threshold.

* `RollTooGreatTermination(max_roll=π/3)`: Ends the episode if the roll exceeds threshold.

* `FastAccelerationTermination()`: Ends the episode if linear or angular velocity explodes.

* `MinimumHeightTermination(min_height=0.8)`: Simpler version of Z-checking.

* `FarFromOriginTermination(max_dist=10.0)`: Treats reaching far distances as success.

* `IllegalContactTermination.create(geom_names=["head", "arm"])`: Ends the episode if certain geoms collide.

You can mix and match termination conditions by returning a list in `get_terminations()`.

***

## Resets

Resets define how to initialize the environment at the beginning of each episode. Every reset subclass implements:

```python
def __call__(self, data: PhysicsData, curriculum_level: jax.Array, rng: jax.random.PRNGKeyArray) -> PhysicsData:
    ...
```

This function receives the current MuJoCo data object and should return a modified version with updated `qpos` and/or `qvel`.

***

### Example Resets

* `RandomJointPositionReset(scale=0.01)`: Adds noise to joint angles.

* `RandomJointVelocityReset(scale=0.01)`: Adds noise to joint velocities.

* `RandomBaseVelocityXYReset(scale=0.01)`: Adds horizontal velocity noise to the root.

* `PlaneXYPositionReset(...)`: Places the root body randomly within XY bounds on a flat surface.

* `HFieldXYPositionReset(...)`: Same as above but uses a heightfield for Z height.

* `InitialMotionStateReset(...)`: Loads initial pose and velocity from a motion dataset (for imitation or motion bootstrapping).

***

## Rewards

Unlike commands, terminations, and resets—which operate on single transitions—**rewards are computed over full trajectories**. This allows you to define dense, sparse, smooth, or event-based signals for learning.

To implement a reward, subclass `Reward` and implement:

```python
def get_reward(self, trajectory: Trajectory) -> jax.Array:
    ...
```

This method should return a reward for each timestep in the trajectory (i.e., shape `(T,)`).

If your reward needs an internal state that persists across rollouts (e.g., for computing jerk or contact over time), use the `StatefulReward` subclass instead and implement:

```python
def initial_carry(self, rng: PRNGKeyArray) -> PyTree:
    ...

def get_reward_stateful(self, trajectory: Trajectory, reward_carry: PyTree) -> tuple[Array, PyTree]:
    ...
```

All rewards support a `.scale` field to scale the magnitude of the reward, and KSim will throw a warning if this scale is not aligned with the name (`Reward` should be positive, `Penalty` should be negative).

***

### Example Rewards

* `StayAliveReward()`: +1 for every step alive, with -1 on failure.

* `LinearVelocityReward(index="x")`: Incentivizes forward velocity.

* `AngularVelocityPenalty(index="z")`: Penalizes rotational speed.

* `BaseHeightReward(height_target=1.1)`: Encourages maintaining a desired height.

* `FeetNoContactReward(window_size=5)`: Reward for lifting feet off ground periodically.

* `JointVelocityPenalty(norm="l2")`: Penalizes rapid joint velocity changes.

* `ActionSmoothnessPenalty(norm="l2")`: Penalizes jerkiness in actions.

* `FeetFlatReward()`: Encourages keeping feet parallel to the floor.

* `JoystickReward()`: Follows high-level discrete joystick commands (0=stop, 1=forward, etc).

* `PositionTrackingReward(...)`: Tracks distance between body and a goal position.

* `BaseJerkZPenalty(ctrl_dt=0.01)`: Penalizes vertical jerk (requires acceleration observation).

* `AvoidLimitsReward(joint_limits=..., joint_limited=...)`: Encourages staying away from joint limits.

* `ObservationMeanPenalty(observation_name="some_obs")`: Penalizes large average observation values.

***

## Events

Events are triggered at arbitrary simulation time (not control steps), and are typically used to perturb the environment. Events are applied **every physics timestep**, although you may choose to randomly apply them only a certain percentage of the time.

Each event must subclass `Event` and implement:

```python
def __call__(...) -> tuple[PhysicsData, Array]:
    ...
    
def get_initial_event_state(self, rng: PRNGKeyArray) -> Array:
    ...
```

***

### Example Events

* `PushEvent(...)`: Applies a random external force after a random interval.

* `JumpEvent(...)`: Launches the robot vertically by modifying vertical velocity.

***

## Curriculum

Curriculum strategies are used to modulate task difficulty during training. They are invoked **once per training epoch**, and return a scalar level in `[0, 1]`.

To implement a curriculum, subclass `Curriculum` and implement:

```python
def __call__(
    self,
    trajectory: Trajectory,
    rewards: RewardState,
    training_state: xax.State,
    prev_state: CurriculumState,
) -> CurriculumState:
    ...

def get_initial_state(self, rng: PRNGKeyArray) -> CurriculumState:
    ...
```

***

### Example Curricula

* `ConstantCurriculum(level=0.0)`: Fixed difficulty.

* `LinearCurriculum(step_size=0.01)`: Increases linearly every few epochs.

* `EpisodeLengthCurriculum(...)`: Increases difficulty if agents survive longer.

* `DistanceFromOriginCurriculum(...)`: Increases difficulty with distance.

* `RewardLevelCurriculum(...)`: Adjusts difficulty based on a reward's average.

* `StepWhenSaturated(...)`: Adjusts difficulty based on death/success saturation.