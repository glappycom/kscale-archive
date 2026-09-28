<!-- preserved from https://docs.kscale.dev/software/simulation/rl via https://web.archive.org/web/20241015000252id_/https://docs.kscale.dev/software/simulation/rl -->

# Rl - K-Scale Labs Docs

Software

Simulation

Policy Training

⚠️

This documentation is under construction and incomplete. Please [sign up here for K-Scale updates (opens in a new tab)](https://forms.gle/xkba4WWGD5Pmayj96) and check back later for our progress.

## Minimal PPO Implementation

[GitHub (opens in a new tab)](https://github.com/kscalelabs/minppo)

A minimal implementation of Proximal Policy Optimization (PPO) utilizing JAX in just three files. Users can import their own custom Mujoco environemnts, define their rewards, and train their own agents with ease.

With this pipeline, we can train agents to perform basic tasks with complete understanding of the underlying training loop, rewards, and physics. Compared to Isaac Gym, this pipeline is much more easier to understand, lightweight, and therefore hackable for research settings.

Here's a video with some basic walking/standing with a humanoid robot:

[Isaac Gym](/software/simulation/isaac "Isaac Gym")[Web Assembly](/software/simulation/wasm "Web Assembly")
