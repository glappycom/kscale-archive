<!-- preserved from https://docs.kscale.dev/docs/exporting via https://web.archive.org/web/20250910205742id_/https://docs.kscale.dev/docs/exporting -->

# Export

Guide to exporting a model to K-Infer format

[PyTorch

PyTorch unit test](https://github.com/kscalelabs/kinfer/blob/master/tests/test_pytorch.py)[Jax

Jax unit test](https://github.com/kscalelabs/kinfer/blob/master/tests/test_jax.py)

## Export

`kinfer` matches the function argument names to inputs which can be gathered from the robot. Currently the following argument names are supported:

* `joint_angles` The robot joint angles, in radians
* `joint_angular_velocities` The robot joint angular velocities, in radians per second
* `projected_gravity` The 3-dimensional projected gravity vector, with magnitude ~9.81
* `accelerometer` The accelerometer readings, in meters per second squared
* `gyroscope` The gyroscope readings, in radians per second
* `command` An N-dimensional command vector
* `carry` The model carry

Note that the model should expect the input tensors to have these shapes.

### Jax

To convert a Jax model to `kinfer` format:

Python

```
import jax
from jax import numpy as jnp

from kinfer.export.jax import export_fn
from kinfer.export.serialize import pack

JOINT_NAMES = ["left_arm", "right_arm", "left_leg", "right_leg"]
NUM_JOINTS = len(JOINT_NAMES)
CARRY_SIZE = 10

@jax.jit
def init_fn() -> jnp.ndarray:
    return jnp.zeros((CARRY_SIZE,))

@jax.jit
def step_fn(
    joint_angles: jnp.ndarray,
    joint_angular_velocities: jnp.ndarray,
    projected_gravity: jnp.ndarray,
    accelerometer: jnp.ndarray,
    gyroscope: jnp.ndarray,
    carry: jnp.ndarray,
) -> tuple[jnp.ndarray, jnp.ndarray]:
    output = (
        joint_angles.mean()
        + joint_angular_velocities.mean()
        + projected_gravity.mean()
        + accelerometer.mean()
        + gyroscope.mean()
        + carry.mean()
    ) * joint_angles
    next_carry = carry + 1
    return output, next_carry

init_fn_onnx = export_fn(
  model=init_fn,
)

step_fn_onnx = export_fn(
  model=step_fn,
  num_joints=len(JOINT_NAMES),
  carry_shape=(CARRY_SIZE,),
)

kinfer_model = pack(
  init_fn_onnx,
  step_fn_onnx,
  joint_names=JOINT_NAMES,
  carry_shape=(CARRY_SIZE,),
)

# Saves the model to disk.
root_dir = Path("~").expanduser()
(kinfer_path := root_dir / "model.kinfer").write_bytes(kinfer_model)
```

### PyTorch

To convert a PyTorch model to `kinfer` format:

Python

```
import torch
from torch import Tensor

from kinfer.export.pytorch import export_fn
from kinfer.export.serialize import pack

JOINT_NAMES = ["left_arm", "right_arm", "left_leg", "right_leg"]
NUM_JOINTS = len(JOINT_NAMES)
CARRY_SIZE = 10

@torch.jit.script
def init_fn() -> Tensor:
    return torch.zeros((CARRY_SIZE,))

@torch.jit.script
def step_fn(
    joint_angles: Tensor,
    joint_angular_velocities: Tensor,
    projected_gravity: Tensor,
    accelerometer: Tensor,
    gyroscope: Tensor,
    carry: Tensor,
) -> tuple[Tensor, Tensor]:
    output = (
        joint_angles.mean()
        + joint_angular_velocities.mean()
        + projected_gravity.mean()
        + accelerometer.mean()
        + gyroscope.mean()
        + carry.mean()
    ) * joint_angles
    next_carry = carry + 1
    return output, next_carry

init_fn_onnx = export_fn(
  model=init_fn,
)

step_fn_onnx = export_fn(
  model=step_fn,
  num_joints=len(JOINT_NAMES),
  carry_shape=(CARRY_SIZE,),
)

kinfer_model = pack(
  init_fn_onnx,
  step_fn_onnx,
  joint_names=JOINT_NAMES,
  carry_shape=(CARRY_SIZE,),
)

# Saves the model to disk.
root_dir = Path("~").expanduser()
(kinfer_path := root_dir / "model.kinfer").write_bytes(kinfer_model)
```

Updated 4 months ago

---

[K-Infer](/docs/k-infer)[Simulate](/docs/simulate)

Ask AI

* [Table of Contents](#)
* + [Export](#export)
  + - [Jax](#jax)
    - [PyTorch](#pytorch)
