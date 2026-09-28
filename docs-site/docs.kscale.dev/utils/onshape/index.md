<!-- preserved from https://docs.kscale.dev/utils/onshape via https://web.archive.org/web/20241218231350id_/https://docs.kscale.dev/utils/onshape -->

# Onshape to URDF Converter - K-Scale Docs

UtilitiesOnshape to URDF

# Onshape to URDF Converter

```
pip install kscale-onshape-library
```

This library is what we use at K-Scale for interacting with OnShape. It is a wrapper around the OnShape API that allows us to easily import parts from OnShape into our projects.

[Github](https://github.com/kscalelabs/onshape)

Here is an example of a robot converted using the `kol` CLI, with the input OnShape model on the right and the output URDF on the left.

![Onshape to URDF](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fonshape2urdf_example.6bfe26aa.png&w=3840&q=75)

To reproduce the above example, you can run the following command:

```
kol run https://cad.onshape.com/documents/3037473d78845106e95befb1/w/e3a76b21fff5430d0e9ecfb5/e/1d74e2fed25abed64482828a --output-dir robot
```

## Installation

```
pip install kscale-onshape-library
pip install 'kscale-onshape-library @ git+https://github.com/kscalelabs/onshape.git@master'  # Install from Github
pip install 'kscale-onshape-library[all]'  # Install all dependencies
```

In order to access the OnShape API, you need to define `ONSHAPE_ACCESS_KEY` and `ONSHAPE_SECRET_KEY` using a key generated [here](https://dev-portal.onshape.com/keys).

## Usage

The KOL CLI provides several subcommands for different operations:

```
kol <subcommand> [options]
```

Available subcommands:

* `run`: Download from Onshape and post-process
* `download`: Only download from Onshape
* `postprocess`: Post-process an existing URDF
* `pybullet`: Run PyBullet simulation

### Download and Post-process

To download a model from Onshape and apply post-processing:

```
kol run <onshape-document-url> (--output-dir <output-directory>)
```

To see additional configuration options, consult the config file [here](https://github.com/kscalelabs/onshape/blob/master/kol/onshape/config.py).

### Download Only

To only download a model from Onshape without post-processing:

```
kol download <document-url> (--output-dir <output-directory>)
```

Options are similar to the `run` subcommand.

### Post-process Existing URDF

To apply post-processing to an existing URDF file:

```
kol postprocess <urdf-path>
```

### PyBullet Simulation

To run a PyBullet simulation with the processed URDF:

```
kol pybullet <urdf-path> [options]
```

## Simulation

The output of the onshape library is simply a robot floating in space. Luckily, most simulators which support URDFs are able to define an environment within code. More changes are needed to make MJCF files simulation ready. The pipeline also generates an MJCF file by default.

Support for other file formats like USD files for IsaacLab will be helpful as well.

## Other Links

* [OnShape API explorer](https://cad.onshape.com/glassworks/explorer/#/Assembly/getFeatures)
* [OnShape API documentation](https://onshape-public.github.io/docs/api-intro/)
* [OnShape-to-Robot Library](https://github.com/Rhoban/onshape-to-robot)

[Introduction](/teleop/intro "Introduction")[URDF to Mujoco](/utils/urdf2mjcf "URDF to Mujoco")
