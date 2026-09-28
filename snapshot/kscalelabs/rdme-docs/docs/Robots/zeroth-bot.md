---
title: Z-Bot
excerpt: The world's most affordable and open-source humanoid robot.
deprecated: false
hidden: false
metadata:
  robots: index
---
Zeroth Bot, or Z-Bot, is an open-source humanoid robot development platform designed for developers and researchers, made for advanced ML and software applications development.

# Motor ID Mappings

<Image align="center" src="https://files.readme.io/0fd0e4a199ec07382b7cbcfcd0c623d4e7ec178c650898664934d1fed12bc624-Zeroth_Bot_Motor_Join_ID_Diagram.png" />

# Robot Composition

The Zeroth Bot consists of head, torso, arms, and legs, with total 16 DoFs, allowing for flexible movement and control:

* Each arm has 3 DoF + 1 DoF Gripper
* Each leg has 6 DoF
* Battery, IMU, camera, microphone, and speaker are installed in the torso

# Robot Functions

* Omnidirectional walking
  * Supports forward, backward, and lateral walking
  * Supports rotation and complex walking
* Disturbance Resistance While Walking
  * Can walk on uneven surfaces
  * Can withstand certain impact disturbances while walking
* Predefined Actions
  * Waving
* Safety Protection
  * Automatically enters damping model in uncontrolled states to prevent damage
  * Hard emergency stop
  * Soft emergency stop