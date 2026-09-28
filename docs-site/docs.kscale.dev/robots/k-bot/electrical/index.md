<!-- preserved from https://docs.kscale.dev/robots/k-bot/electrical/ via https://web.archive.org/web/20251109015646id_/https://docs.kscale.dev/robots/k-bot/electrical/ -->

# Electrical System | K-Scale Docs

* [Robots](/category/robots)
* [K-Bot](/category/k-bot)
* Electrical System

On this page

# Electrical System

note

The K-Bot hardware and software is still under active development and improvement.

**License**
The hardware components of this project are licensed under CERN-OHL-S while the software components are licensed under GPL v3, unless otherwise specified. See [LICENSE-HW](https://github.com/kscalelabs/kbot/blob/master/LICENSE-HW) and [LICENSE](https://github.com/kscalelabs/kbot/blob/master/LICENSE), respectively.

This guide explains a little bit about how the electrical system is structured.

## Overview[​](#overview "Direct link to Overview")

The main battery connector has a 80A fuse. The smaller wires in the connector are used for the battery management system (BMS).
Three main items need to be plugged into the powerboard or it will start beeping. The power button (neon green), the e-stop (orange), and the power resistor (light blue). Each link of the robot needs to be plugged in to the 48V + CAN lines (purple). There are 2 additional CAN lines that provide 24V as shown in (pink). Finally, there is an additional 24V header that we use to power the Raspberry Pi 5 using a buck converter. The USB A should be connected to the Raspberry Pi via a male USB A to male USB A cable.

![Powerboard](/assets/images/powerboard-af6c89978faa6054b3cfa2b4cf8dad28.png)

![Connectors](/assets/images/connectors-4550f4cf855514ff75d98db8961cccc7.png)

[Edit this page](https://github.com/kscalelabs/docs/tree/main/docs/robots/k-bot/electrical.md)
