---
title: Task
excerpt: Getting started defining your own RL tasks
deprecated: false
hidden: false
metadata:
  robots: index
---
# Defining a Task

In KSim, a **task** defines the environment and training logic. KSim provides multiple battle-tested tasks that implement standard training logic (e.g. `PPOTask`, `AMPTask`, etc.), but it is also easy to define your own task to suit advanced training requirements. This article covers how to implement a KSim task and update underlying training logic via config parameterization.

***

## Abstract Methods

Similar to the API of PyTorch Lightning, you can define a task by implementing a set of abstract methods. While not exhaustive, there are roughly 3 types of abstract methods that must be implemented:

* **Environment-specific methods:** randomize physics, load robot model, simulate actuators, create observations, define rewards, etc.
* **Model-specific methods:** get the policy, sample actions, etc.
* **Algorithm-specific methods:** model update or bespoke algorithm-specific methods from a class that already implements the model update)

By default, all KSim tasks support parallel rollout logic, logging utilities, visualization tools, and the core training loop. Ultimately, KSim gives you great freedom to define exactly how you'd like your training to happen.

### Environment-Specific Methods

* `get_mujoco_model`: This should return either an `mjx.Data` or `mujoco.MjModel` object, which represents the physical model of the environment. The type of the returned model ultimately determines the engine used during training (e.g. mjx, mujoco, and potentially other mujoco-like engines). It is called during the initialization of the environment to set up the simulation.

* `get_actuators`: This returns an `Actuators` object, which defines the actuators available in the environment (e.g. position control, MIT style, etc.). While not required, we recommend setting all actuators to torque-driven `<motor/>` actuators, as the `Actuator` object is designed to produce torques as outputs. It is used during the setup of the physics engine to control the environment's dynamics.

* `get_observations`: This returns a collection of `Observation` objects, which generate a policy-facing observation dictionary from the environment state. It is called during the rollout phase to gather observations from the environment.

* `get_commands`: This returns a collection of `Command` objects, which define the commands that can be issued to the policy (e.g. desired base velocity, direction, etc.). It is used during the rollout phase to determine the actions taken by the agent.

* `get_terminations`: This returns a collection of `Termination` objects, which define the conditions under which an episode terminates. It is used during the rollout phase to determine when an episode should end.

* `get_resets`: This returns a collection of `Reset` objects, which define how the environment is reset at the beginning of an episode. It is called during the rollout phase after a termination to reset the environment for the next episode.

* `get_events`: This returns a collection of `Event` objects, which define events that can occur in the environment (e.g. a push event). It is used to trigger specific actions or changes in the environment during training.

* `get_rewards`: This returns a collection of `Reward` objects, which define the reward signals provided by the environment. It is called immediately after rollout on the `Trajectory` object to provide learning signal for training.

* `get_curriculum`: This returns a `Curriculum` object, which defines the progression of difficulty in the environment. It is used to adjust the environment's parameters (e.g. event frequency) over time to facilitate learning.

* `get_physics_randomizers`: This returns a collection of `PhysicsRandomizer` objects, which define how the environment's physics can be randomized. It is used to introduce variability in the environment during training. For now, each parallel environment has its own randomization that is defined at the start of training (though this might change).

### Model-Specific Methods

* `get_model`: This returns a PyTree-like object which holds the learnable weights and / or the static control logic. The model gets updated during training, and the user defines exactly how to use this object to perform sampling. As such, KSim supports Flax, Equinox, and most other neural network libraries.

* `get_optimizer`: This returns an `optax` optimizer object, which gets initialized at the start of training. It is intended for `model_udpate` to interact with the optimizer.

* `sample_action`: This is responsible for sampling an action from the model given the current state of the environment. It is called during the rollout phase to determine the agent's actions. You return an `Action` object, which includes the model carry and auxiliary outputs. As a refresher, model carries can be used to store the recurrent states, and auxiliary variables can be used as information for rewards.

### Algorithm-Specific Methods

* `update_model`: This updates the model based on the collected trajectories and rewards. It is called after the rollout phase, during the training loop, to improve the model's performance. Algorithms such as Proximal Policy Optimization (PPO) implement the update\_model function but require additional features. For example, they may need to implement functions like `get_ppo_variables` to handle specific aspects of the PPO algorithm. For more details, see the section on Core Algorithms / PPO.

***

## Config Items

The `RLConfig` class contains all the configuration items needed to define and control the behavior of an RL task in KSim. Here's a summary of key configuration items, grouped by purpose:

### Viewer & Visualization

* `run_model_viewer`: Whether to run the environment viewer loop instead of training.

* `run_model_viewer_argmax_action`: Whether to use argmax policy when running the viewer.

* `run_viewer_num_seconds`: Number of seconds to run the viewer (None means manual quit).

* `run_viewer_save_renders`: If True, saves each frame as an image.

* `run_viewer_save_video`: If True, saves the trajectory as a `.gif` or `.mp4` video.

### Dataset Collection

* `collect_dataset`: If True, collect a dataset instead of training.

* `dataset_num_batches`: Number of batches of trajectories to collect.

* `dataset_save_path`: Optional path to save the collected dataset.

* `collect_dataset_argmax_action`: Whether to use argmax action during dataset collection.

### Logging

* `log_train_metrics`: Whether to log metrics during training.

* `epochs_per_log_step`: Number of epochs between logging steps.

* `profile_memory`: Whether to profile memory usage during training.

### Training Parameters

* `num_envs`: Number of parallel environments to simulate.

* `batch_size`: Number of updates per rollout batch.

* `rollout_length_seconds`: Duration of each environment rollout.

### Evaluation / Validation

* `valid_every_n_seconds`: Frequency (in seconds) to run full validation.

* `valid_first_n_seconds`: When to run first validation after start.

* `render_full_every_n_steps`: Number of valid steps between full renders.

### Rendering Configuration

* `max_values_per_plot`: Max number of series plotted per variable.

* `plot_figsize`: Size of matplotlib plots.

* `render_with_glfw`: If None, auto-detect GLFW availability.

* `render_shadow`: Render with shadow.

* `render_reflection`: Render with reflection.

* `render_contact_force`: Show contact forces.

* `render_contact_point`: Show contact points.

* `render_inertia`: Show inertia visualization.

* `render_height_small`, `render_width_small`: Dimensions of small viewer window.

* `render_height`, `render_width`: Dimensions of full render window.

* `render_length_seconds`: Duration of evaluation render.

* `render_fps`: FPS for the rendered video.

* `render_slowdown`: Slowdown factor for video replay.

* `render_track_body_id`: Body ID to track with camera.

* `render_distance`, `render_azimuth`, `render_elevation`, `render_lookat`: Camera configuration.

* `render_markers`: Whether to draw debug markers.

* `render_camera_name`: Which camera to use by name or ID.

### Physics Engine Parameters

* `ctrl_dt`: Control loop timestep.

* `dt`: Physics simulation timestep.

* `tolerance`: Solver tolerance.

* `iterations`: Max iterations for main solver.

* `ls_iterations`: Line search iterations (for CG/Newton solvers).

* `solver`: Solver type (e.g., 'newton').

* `integrator`: Integrator type (e.g., 'implicitfast').

* `disable_euler_damping`: Improves perf by disabling damping.

* `max_action_latency`: Max action latency for sim.

* `reward_clip_min`, `reward_clip_max`: Clip reward values.

This configuration is designed to be flexible and accommodate the needs of a wide range of reinforcement learning experiments in KSim. You can extend or modify it depending on your specific task or engine setup.