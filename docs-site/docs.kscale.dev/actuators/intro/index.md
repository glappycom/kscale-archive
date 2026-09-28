<!-- preserved from https://docs.kscale.dev/actuators/intro via https://web.archive.org/web/20241111163107id_/https://docs.kscale.dev/actuators/intro -->

# Actuator Package - K-Scale Docs

ActuatorsIntroduction

# Actuator Package

```
sudo apt install pkg-config libudev-dev  # If not installed
pip install actuator
```

`actuator` is a Python and Rust package developed by K-Scale Labs to make it easy to control robot actuators.

[Code](https://github.com/kscalelabs/actuator)[Support](https://discord.gg/kscale)[Forum](https://forum.kscale.dev)

Here is a high-level overview of the package architecture.

![Actuator Package Architecture](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Farchitecture.8a42fc1f.png&w=3840&q=75)

## Getting Started

### Prerequisites

* **Operating System**: This package has been tested on Linux, but may work with other operating systems.
* **Python**: Python 3.11 or later.
* **Rust**: This package has been tested with Rust 1.80.1, but will likely work with other versions.

You should install the following libraries:

```
sudo apt install pkg-config libudev-dev
```

### Installation

The package can easily be installed from PyPI using the command:

```
pip install actuator
```

Alternatively, to install the bleeding edge version from Github, use the command:

```
pip install 'actuator @ git+https://github.com/kscalelabs/actuator.git@master'
```

#### Actuator-Specific requirements

Note that some actuators have additional requirements. See the individual actuator pages for more information.

[Robstride](/actuators/robstride)

[Code Signing](/os/signing "Code Signing")[Robstride](/actuators/robstride "Robstride")
