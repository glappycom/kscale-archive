<!-- preserved from https://docs.kscale.dev/software/simulation/wasm via https://web.archive.org/web/20241014235901id_/https://docs.kscale.dev/software/simulation/wasm -->

# Wasm - K-Scale Labs Docs

Software

Simulation

Web Assembly

⚠️

This documentation is under construction and incomplete. Please [sign up here for K-Scale updates (opens in a new tab)](https://forms.gle/xkba4WWGD5Pmayj96) and check back later for our progress.

## MuJoCo Web Assembly

[Our GitHub (opens in a new tab)](https://github.com/nathanjzhao/interactive-mujoco)

Stompy Live allows for users to interact directly with our URDF models in a MuJoCo simulation within the browser, with the ability to add peturbations, conduct IK on end effectors, and play/pause the simulation at certain frames. Beyond this, we are exporting our models trained from [MinPPO](/software/simulation/minppo) to Tensorflow.js to allow for real-time inference and playback of the trained models.

To view interact with the simulation, please visit the website [here (opens in a new tab)](https://nathanzhao.cc/interactive-mujoco/).

Longterm, this would be useful to test the robustness and generalizability of our models, and will also help us to understand the limitations of our current models as we can directly peturb our model in simulation.

[Policy Training](/software/simulation/rl "Policy Training")[Overview](/software/teleop/overview "Overview")
