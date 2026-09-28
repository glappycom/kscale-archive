---
title: Troubleshooting
excerpt: A living document of issues that we have encountered while using K-Sim
deprecated: false
hidden: false
metadata:
  robots: index
---
# Troubleshooting

## Headless Systems

When you try to render a trajectory while on a headless system, you may get an error like the following:

```bash
mujoco.FatalError: an OpenGL platform library has not been loaded into this process, this most likely means that a valid OpenGL context has not been created before mjr_makeContext was called
```

The fix is to create a virtual display:

```bash
Xvfb :100 -ac &
PID1=$!
export DISPLAY=:100.0
```

You may also need to tell MuJoCo to use GPU accelerated off-screen rendering via

```
export MUJOCO_GL="egl"
```

## NaNs when running example policy

This manifests sometimes when you have an error like this:

`Registers are spilled to local memory in function`

We have observed this happening when training on RTX 4090s. To mitigate, disable Triton GEMM kernels:

```shell
export XLA_FLAGS='--xla_gpu_enable_latency_hiding_scheduler=true --xla_gpu_enable_triton_gemm=false'
```

Then, you may need to remove your JAX cache to trigger JAX to rebuild the kernels:

```shell
rm -r ~/.cache/jax/jaxcache
```

We've found that removing the cache can fix a number of otherwise-mysterious errors.

## NaNs during training

Seeing NaNs when training a new policy is always frustrating. We have implemented a few tools in ksim to help debug such NaNs. Here is our suggested workflow:

1. Make sure you are regularly saving checkpoints.
2. When you start seeing NaNs, kill your training job.
3. Re-run the training job initializing from the same checkpoint

```Text bash
JAX_DEBUG_NANS=True DISABLE_JIT_LEVEL=10 python -m examples.walking exp_dir=/path/to/exp/dir/run_N
```

This will disable JIT'ting the training pass of your neural network while keeping the MJX environment step JIT'ted, while also throwing an error the first time that JAX encounters a NaN.

## General Training Issues

If you're experiencing issues with training recurrent models, it's important to double check exactly how the carry term progresses through training. Specifically, check that the carry term in `sample_action` gets produced in a similar way when getting off-policy training variables.