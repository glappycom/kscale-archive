<!-- preserved from https://docs.kscale.dev/pkg/python via https://web.archive.org/web/20241214035733id_/https://docs.kscale.dev/pkg/python -->

# kscale Python API - K-Scale Docs

[Platform](/pkg/intro "Platform")Python

# `kscale` Python API

⚠️

This API is currently under construction.

The Python API lets you interact with the K-Scale platform programmatically.

## Usage

Here is an example of how to use the Python API to upload and download URDF files. Note that there are both asynchronous and synchronous versions of each function. The asynchronous version is preferred for performance (the synchronous version simply wraps the asynchronous version with `asyncio.run`).

```
import asyncio
from kscale import K
 
async def main() -> None:
    api = K()
 
    # Upload a URDF file to the K-Scale platform.
    await api.upload_urdf("listing_id", Path("path/to/urdf/root/"))  # Asynchronous version
    api.upload_urdf_sync("listing_id", Path("path/to/urdf/root/"))  # Synchronous version
 
    # Download and cache the URDF file from the K-Scale platform.
    urdf_path = await api.urdf_path("artifact_id")  # Asynchronous version
    urdf_path = api.urdf_path_sync("artifact_id")  # Synchronous version
 
if __name__ == "__main__":
    asyncio.run(main())
```

[Command Line Interface](/pkg/cli "Command Line Interface")[kInfer](/models/kinfer "kInfer")
