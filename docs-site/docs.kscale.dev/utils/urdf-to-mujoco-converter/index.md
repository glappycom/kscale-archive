<!-- preserved from https://docs.kscale.dev/utils/urdf-to-mujoco-converter/ via https://web.archive.org/web/20251014101244id_/https://docs.kscale.dev/utils/urdf-to-mujoco-converter/ -->

# Onshape to URDF Converter | K-Scale Docs

* [Utils](/category/utils)
* Onshape to URDF Converter

On this page

See the source code for this repository [here](https://github.com/kscalelabs/onshape) .

# Getting Started

## Dependencies[​](#dependencies "Direct link to Dependencies")

The `onshape` package requires Python 3.11 or greater.

## Installation[​](#installation "Direct link to Installation")

`onshape` can be installed through `pip` using the following command:

```
pip install onshape  # To install the vanilla version  
pip install 'onshape[all]'  # To install with all dependencies
```

Verify that the package was installed correctly by checking that the `onshape` CLI is available:

```
$ onshape  
usage: onshape {run,download,postprocess,pybullet,mujoco}  
onshape: error: the following arguments are required: subcommand
```

Next, you should retrieve an Onshape Access Key and Secret Key from [here](https://cad.onshape.com/appstore/dev-portal) . Set the required environment variables like so:

```
export ONSHAPE_ACCESS_KEY='XXXXXXXXXXXXXXXXXXXXXXXX'  
export ONSHAPE_SECRET_KEY='YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
```

# Usage

The Onshape CLI has the following components:

* `download` - takes a link to an Onshape assembly and downloads it as a URDF
* `postprocess` - takes a path to a downloaded URDF and applies postprocessing to make it useful
* `run` - Combines `download` and `postprocess` into a single script
* `pybullet` - Opens a Pybullet visualization of a generated URDF file, for debugging purposes
* `mujoco` - Opens a Mujoco visualization of a generated MJCF file, for debugging purposes

## Download[​](#download "Direct link to Download")

To download a URDF file, use the following command:

```
$ onshape download --help  
usage: onshape [-h] [-o OUTPUT_DIR] [-f CONFIG_PATH] [-n] document_url  
  
positional arguments:  
  document_url          The URL of the OnShape document.  
  
options:  
  -h, --help            show this help message and exit  
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR  
                        The output directory.  
  -f CONFIG_PATH, --config-path CONFIG_PATH  
                        The path to the config file.  
  -n, --no-cache        Disables caching.
```

You can override configuration options from the command line by passing the values using [omegaconf syntax](https://omegaconf.readthedocs.io/) or by providing a configuration file.

## Postprocess[​](#postprocess "Direct link to Postprocess")

To postprocess a downloaded URDF file, use the following command:

```
$ onshape postprocess --help  
usage: onshape [-h] [-f CONFIG_PATH] urdf_path  
  
positional arguments:  
  urdf_path             The path to the downloaded URDF.  
  
options:  
  -h, --help            show this help message and exit  
  -f CONFIG_PATH, --config-path CONFIG_PATH  
                        The path to the config file.
```

You can override the postprocess configuration arguments in the same way.

## Config File Reference[​](#config-file-reference "Direct link to Config File Reference")

To view all the available configuration options, see [this file](https://github.com/kscalelabs/onshape/blob/master/onshape/onshape/config.py) .

**Ignore Welding Joints**

By default, fixture joints on the same body gets combined into one body. To avoid this you can set the following params:

```
ignore_merging_fixed_joints:  
  - "imu_link"
```

or

```
merge_fixed_joints: false
```

# FAQ

How to update permission? After requesting permissions, remove ~/.kscale/

# Additional Resources

## Get Help[​](#get-help "Direct link to Get Help")

* [Github Issues](https://github.com/kscalelabs/onshape/issues)

## OnShape API[​](#onshape-api "Direct link to OnShape API")

* [OnShape API Explorer Glassworks](https://cad.onshape.com/glassworks/explorer/)
* [OnShape API Documentation](https://onshape-public.github.io/docs/api-intro/)

## Other Tools[​](#other-tools "Direct link to Other Tools")

* [Rhoban's Onshape-to-Robot Github](https://github.com/Rhoban/onshape-to-robot)

[Edit this page](https://github.com/kscalelabs/docs/tree/main/docs/utils/urdf-to-mujoco-converter.md)
