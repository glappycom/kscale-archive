<!-- preserved from https://docs.kscale.dev/os/rtos via https://web.archive.org/web/20241214051036id_/https://docs.kscale.dev/os/rtos -->

# Real-Time Operating System - K-Scale Docs

[Operating System](/os/intro "Operating System")Real-Time OS

# Real-Time Operating System

⚠️

This page is currently under construction.

Here are some high-level notes about the architecture of the real-time operating system:

* We build the full Linux kernel for K-Scale OS using our own extensions to Buildroot
* The main control loop is implemented as a daemon process that runs at boot, using the `SCHED_RR` scheduling class
* We enable `PREEMPT_RT` to ensure that we can meet our hard real-time requirements
* The control loop itself is implemented in Rust, which exposes an gRPC interface over HTTP for communicating with other components
  + We implement a Python API for interacting with the HTTP server from userspace, allowing users to upload Klang programs

[Klang](/os/klang "Klang")[Python SDK](/os/sdk "Python SDK")
