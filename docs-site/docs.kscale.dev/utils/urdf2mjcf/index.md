<!-- preserved from https://docs.kscale.dev/utils/urdf2mjcf via https://web.archive.org/web/20241111173340id_/https://docs.kscale.dev/utils/urdf2mjcf -->

# URDF to Mujoco Converter - K-Scale Docs

[Utilities](/utils/onshape "Utilities")URDF to Mujoco

# URDF to Mujoco Converter

```
pip install urdf2mjcf
```

`urdf2mjcf` is a tool for converting URDF models to Mujoco XML.

[Github](https://github.com/kscalelabs/urdf2mjcf)

Here is an example, with the input URDF on the right and the output MJCF on the left:

![URDF to MJCF](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Furdf2mjcf_example.0da7ea2a.png&w=3840&q=75)

## Installation

You can install the package using `pip`:

```
pip install urdf2mjcf
```

## Usage

### Command Line

To run the conversion script from the command line, use:

```
urdf2mjcf path/to/your/robot.urdf
```

This will save the MJCF file in the same directory as the URDF file.

To see all the options, use:

```
urdf2mjcf -h
```

### Python

To run the conversion script from Python, use:

```
from urdf2mjcf import run
 
run(
    urdf_path="path/to/your/robot.urdf",
    mjcf_path="path/to/save/robot.mjcf",
    copy_meshes=True,
)
```

[Onshape to URDF](/utils/onshape "Onshape to URDF")[Color Logging](/utils/colorlogging "Color Logging")
