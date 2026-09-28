"""Utility functions for telemetry package."""

import asyncio
import json
import logging
from pathlib import Path
from typing import Sequence, Tuple

from kscale import K
from kscale.web.gen.api import RobotURDFMetadataOutput
from kscale.web.utils import get_robots_dir, should_refresh_file

from kinfer.rust_bindings import PyModelMetadata
import tarfile

logger = logging.getLogger(__name__)


CONFIG_PATH = Path(__file__).parent / "configs"

__all__ = [
    "load_joint_names",
    "download_robot_assets",
    "get_robot_metadata",
    "download_robot_and_metadata",
]


def load_joint_names(kinfer_file: Path) -> Sequence[str]:
    """Return the ordered list of joint names for *robot*.
    """
    with tarfile.open(kinfer_file, 'r:gz') as tar:
        metadata_file = tar.extractfile('metadata.json')
        metadata_json = metadata_file.read().decode('utf-8')
        metadata = json.loads(metadata_json)
    return metadata['joint_names']


async def download_robot_assets(class_name: str, *, cache: bool = True) -> Path:
    """Download (or reuse) the compressed robot bundle for *class_name*.

    Return the **directory** that now contains:

        robot.urdf
        meshes/…
        textures/…

    The bundle is cached under `~/.kscale/robots/<class_name>/robot/`.
    """
    async with K() as api:
        unpack_dir: Path = await api.download_and_extract_urdf(class_name, cache=cache)

    if not any(unpack_dir.glob("*.urdf")):
        raise FileNotFoundError(f"No *.urdf file found in {unpack_dir}")

    return unpack_dir


async def get_robot_metadata(class_name: str, *, cache: bool = True) -> dict:
    """Retrieve metadata for *class_name* as a plain `dict`.

    Cached in `~/.kscale/robots/<class_name>/metadata.json`.
    """
    metadata_path = get_robots_dir() / class_name / "metadata.json"

    if not (cache and metadata_path.exists() and not should_refresh_file(metadata_path)):
        async with K() as api:
            robot_cls = await api.get_robot_class(class_name)
            if robot_cls.metadata is None:
                raise ValueError(f"No metadata available for robot '{class_name}'")

        metadata_path.parent.mkdir(parents=True, exist_ok=True)
        with metadata_path.open("w") as f:
            json.dump(robot_cls.metadata.model_dump(), f, indent=2)

    with metadata_path.open("r") as f:
        meta_obj = RobotURDFMetadataOutput.model_validate_json(f.read())

    return meta_obj.model_dump()


async def download_robot_and_metadata(class_name: str, *, cache: bool = True) -> Tuple[Path, dict]:
    """Convenience wrapper to fetch both the asset bundle and metadata in parallel.

    Returns:
    -------
    (assets_directory, metadata_dict)
    """
    assets_dir, metadata = await asyncio.gather(
        download_robot_assets(class_name, cache=cache),
        get_robot_metadata(class_name, cache=cache),
    )
    return assets_dir, metadata
