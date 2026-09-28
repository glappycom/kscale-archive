<!-- preserved from https://docs.kscale.dev/pkg/cli via https://web.archive.org/web/20241214034924id_/https://docs.kscale.dev/pkg/cli -->

# The kscale CLI - K-Scale Docs

[Platform](/pkg/intro "Platform")Command Line Interface

# The `kscale` CLI

The `kscale` CLI is what we use to interact with [K-Scale web services](https://kscale.store/).

[Github](https://github.com/kscalelabs/kscale)

This CLI is built in Python and is fully open-source.

### Usage

```
kscale <subcommand> [options]
```

Where `<subcommand>` is either `urdf` or `pybullet`.

### Subcommands

#### URDF

The `urdf` subcommand allows you to manage URDF (Unified Robot Description Format) files in the K-Scale store.

Usage:

```
kscale urdf <command> <artifact_id> [options]
```

Available commands:

* `download`: Download a URDF artifact from the K-Scale store.
* `info`: Display information about a URDF artifact.
* `remove-local`: Remove locally cached URDF files.

##### Examples

1. Download a URDF:

   ```
   kscale urdf download <artifact_id>
   ```
2. Get URDF information:

   ```
   kscale urdf info <artifact_id>
   ```
3. Remove local URDF cache:

   ```
   kscale urdf remove-local <artifact_id>
   kscale urdf remove-local all
   ```

#### PyBullet

The `pybullet` subcommand allows interaction with PyBullet functionalities. The specific commands and options for this subcommand are not provided in the given code snippet.

Usage:

```
kscale pybullet [options]
```

For detailed information on the available commands and options for the `pybullet` subcommand, please refer to the `pybullet.py` file or run:

```
kscale pybullet --help
```

### Notes

* The CLI uses asynchronous operations for improved performance.
* An API key is required for certain operations. Set it as the `KSCALE_API_KEY` environment variable or in your config file.
* The CLI uses a local cache to store downloaded artifacts. The cache location can be configured in the settings.

For more detailed information on each command and its options, use the `--help` flag with any command or subcommand.

[Introduction](/pkg/intro "Introduction")[Python](/pkg/python "Python")
