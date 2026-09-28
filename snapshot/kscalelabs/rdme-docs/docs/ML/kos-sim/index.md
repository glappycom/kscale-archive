---
title: KOS Sim
deprecated: false
hidden: false
metadata:
  robots: index
---
`kos-sim` is a simulation backend for the [K-Scale Operating System (KOS)](https://github.com/kscalelabs/kos), using the same gRPC interface. This lets you try out your KOS programs before deploying them onto a real robot. Once you're ready, you can run your code on the robot just by changing the client IP address.

## Installation

```shell bash
pip install kos-sim
```

## Getting Started

First, start the `kos-sim` backend:

```shell
kos-sim kbot-v1
```

Then, in a separate terminal, run one of the [repository examples](https://github.com/kscalelabs/kos-sim), such as:

```shell
python -m examples.kbot
```

You should see the simulated K-Bot move in response to the client commands.

### K-Scale Assets

To fetch your MJCF from a local repository instead of from the K-Scale api, set the `KSCALE_ASSETS_PATH` environment variable to point to that repo. For example, you can reference the [kscale-assets](https://github.com/kscalelabs/kscale-assets) repository

```shell
export KSCALE_ASSETS_PATH=/path/to/kscale-assets
```