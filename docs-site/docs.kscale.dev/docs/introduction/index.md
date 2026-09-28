<!-- preserved from https://docs.kscale.dev/docs/introduction via https://web.archive.org/web/20250213230159id_/https://docs.kscale.dev/docs/introduction -->

# Introduction to Skills Training

See three different frameworks where you can train your humanoid to learn new skills.

## Introduction

Learning algorithms allow to train humanoids to perform different skills such as manipulation or locomotion. Below is an overview of general approaches to training machine learning models for humanoid robots with example applications. Typically you need a simulator, training framework and machine learning method to train end to end behaviors.

### Simulation Artifacts

To view simulation artifacts, use the K-Scale API:

Text

```
pip install kscale
ks robots list  # To list the available robots
ks robots urdf download <robot-name>  # To download the robot
```

### Physics engines

Physics engines are software libraries designed to simulate physical systems in a virtual environment. They are crucial in a variety of fields such as video games, animation, robotics, and engineering simulations. These engines handle the mathematics involved in simulating physical processes like motion, collisions, and fluid dynamics. Three popular engines are:

* PhysX is a physics engine by NVIDIA used primarily for video games and real-time simulations. It supports rigid body dynamics, cloth simulation, and particle effects, enhancing realism and interactivity in 3D environments.  
  MuJoCo
* MuJoCo (Multi-Joint dynamics with Contact) is a physics engine designed for research in robotics and biomechanics. It's known for its speed, accuracy, and ease of use, making it popular for simulating complex systems with robotics and articulated structures.
* Bullet is a physics engine supporting real-time collision detection and multi-physics simulation for VR, games, visual effects, robotics, machine learning.

### Training frameworks

Given the physical engine, simulators can create environments used to train skill for different humanoids. We support three such popular training frameworks:

[Isaac Lab](https://kscale.readme.io/update/docs/isaac-lab)

[Mujoco Playground](doc:mujoco)

[Genesis](doc:genesis)

## Performance Analysis

Further analysis can be done on the outputs after doing the initial training.

## MJCF Visualizer

To visualize any MJCF file, you can run the following command:

```
python3 -m mujoco.viewer --mjcf \<path-to-mjcf-file>
```

The command above loads MuJoCo’s GUI, which allows you to simulate the model, manually specify joints, and save keyframes.

Updated 26 days ago

---

What’s Next

See three different frameworks where you can train your humanoid to learn new skills.

* [Isaac Lab](/docs/isaac-lab)
* [Genesis](/docs/genesis)
* [Mujoco Playground](/docs/mujoco)

* [Table of Contents](#)
* + [Introduction](#introduction)
  + - [Simulation Artifacts](#simulation-artifacts)
    - [Physics engines](#physics-engines)
    - [Training frameworks](#training-frameworks)
  + [Performance Analysis](#performance-analysis)
  + [MJCF Visualizer](#mjcf-visualizer)
