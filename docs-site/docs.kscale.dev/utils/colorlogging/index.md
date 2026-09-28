<!-- preserved from https://docs.kscale.dev/utils/colorlogging via https://web.archive.org/web/20241111163834id_/https://docs.kscale.dev/utils/colorlogging -->

# Colorful Python Logging - K-Scale Docs

[Utilities](/utils/onshape "Utilities")Color Logging

# Colorful Python Logging

```
pip install colorlogging
```

`colorlogging` is a tool for making Python logging more colorful.

[Github](https://github.com/kscalelabs/colorlogging)

This project is dependency-free and therefore it is very lightweight. Here is an example of colorful logs:

![Example of colorlogging output](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fcolorlogging_example.1c2d9e7f.png&w=1920&q=75)

## Installation

Simply run

```
pip install colorlogging
```

## Usage

To configure logging, call `configure_logging` like so:

```
import colorlogging
import logging
 
logger = logging.getLogger(__name__)
 
def main() -> None:
    colorlogging.configure()
    logger.info("Hello, world!")
```

This tool also provides some other helpful display functions:

```
import colorlogging
 
colorlogging.show_info("This is a status message", important=True)
colorlogging.show_warning("This is a warning message")
colorlogging.show_error("This is an error message")
```

This shows the following output:

![Another example of colorlogging output](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fcolorlogging_example2.b3d58430.png&w=828&q=75)

[URDF to Mujoco](/utils/urdf2mjcf "URDF to Mujoco")[Introduction](/hw/intro "Introduction")
