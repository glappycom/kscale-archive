<!-- preserved from https://docs.kscale.dev/software/klang/intro via https://web.archive.org/web/20241014230545id_/https://docs.kscale.dev/software/klang/intro -->

# Intro - K-Scale Labs Docs

Software

Klang

Introduction

⚠️

This documentation is under construction and incomplete. Please [sign up here for K-Scale updates (opens in a new tab)](https://forms.gle/xkba4WWGD5Pmayj96) and check back later for our progress.

[GitHub (opens in a new tab)](https://github.com/kscalelabs/klang)

## Introduction

Klang is a domain-specific language (DSL) for programming robots. Here, we are working on our parser with Rust. From this, we will hopefully allow users to be able to write Klang code that can be compiled into motor control commands for our robots.

Think Midjourney - we want users to be able to apply various tags for our model to understand implicitly and generate motor control commands.

### Architecture

Below is a diagram showing the architecture of the Klang neural interpreter.

![robot part](/_next/static/media/arch.c4892ade.svg)

[E-VLA](/software/models/evla "E-VLA")[Mujoco](/software/simulation/mujoco "Mujoco")
