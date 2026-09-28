"""URDF visualization and animation utilities using Rerun."""

import argparse
import asyncio
import logging
import math
from pathlib import Path
from typing import Callable, Sequence

import colorlogging
import numpy as np
import numpy.typing as npt
import rerun as rr
import trimesh
import urdfpy
from urdfpy import urdf as _urdf, utils as _u

from telemetry.utils import download_robot_assets

# Set up logger for this module
logger = logging.getLogger(__name__)


def deg(rad: float) -> float:
    """Convert radians to degrees."""
    return math.degrees(rad)


def dump_joint_origins(urdf: urdfpy.URDF) -> None:
    for j in urdf.joints:
        # origin is 4×4 T_child_parent  (joint → parent-link frame)
        transform_matrix: npt.NDArray[np.float64] = np.asarray(j.origin) if j.origin is not None else np.eye(4)
        xyz: npt.NDArray[np.float64] = transform_matrix[:3, 3]
        rpy: npt.NDArray[np.float64] = trimesh.transformations.euler_from_matrix(transform_matrix[:3, :3], axes="sxyz")
        axis: npt.NDArray[np.float64] = np.asarray(j.axis, dtype=float)
        info: str = (
            f"{j.name:25} | {j.joint_type:9} | "
            f"xyz = [{xyz[0]: .4f} {xyz[1]: .4f} {xyz[2]: .4f}] m   "
            f"rpy = [{deg(rpy[0]):6.1f}° {deg(rpy[1]):6.1f}° {deg(rpy[2]):6.1f}°]"
        )
        if j.joint_type in {"revolute", "prismatic"}:
            info += f"   axis = {axis}"
        logger.info(info)


def axis_in_parent(joint: urdfpy.Joint) -> npt.NDArray[np.float64]:
    axis: npt.NDArray[np.float64] = np.asarray(joint.axis).astype(float)  # joint axis in joint frame
    rotation_matrix: npt.NDArray[np.float64] = joint.origin[:3, :3]  # 3×3 rotation from joint→parent
    return (rotation_matrix @ axis).astype(float)


def _patch_mesh_loader(urdf_file: Path) -> None:
    """Monkey-patch urdfpy so every `mesh filename="meshes/foo.stl"` is resolved.

    Relative to the directory that contains `urdf_file`.
    """
    # Keep a reference to the original function so we can still call it:
    orig_load_meshes: Callable[..., object] = _u.load_meshes

    urdf_dir: Path = urdf_file.parent.resolve()

    def load_meshes_fixed(filename: str, *a: object, **kw: object) -> object:
        path: Path = Path(filename)
        if not path.is_absolute():
            path = (urdf_dir / path).resolve()  # <- **only** prepend urdf_dir
        return orig_load_meshes(str(path), *a, **kw)

    # Patch BOTH references inside urdfpy:
    _u.load_meshes = load_meshes_fixed  # utils copy
    _urdf.load_meshes = load_meshes_fixed  # alias used by URDF.load()


def link_entity_path(urdf: urdfpy.URDF, link_name: str, urdf_file: Path) -> str:
    """Return the EntityPath (as a string) that rerun's URDF loader uses for `link_name`.

    * root component     : the URDF file name, e.g. "robot.urdf"
    * intermediate parts : every ancestor link in the kinematic chain
    * last component     : `link_name` itself
    """
    # Build child->parent map once:
    if not hasattr(urdf, "_link_parent"):
        urdf._link_parent = {j.child: j.parent for j in urdf.joints}

    parts: list[str] = [link_name]
    while parts[-1] in urdf._link_parent:  # climb to the root link
        parts.append(urdf._link_parent[parts[-1]])

    parts.reverse()
    return "/".join([urdf_file.name, *parts])  # prepend "robot.urdf"


class UrdfTree:
    """Python clone of the Rust helper from the Rerun repo."""

    def __init__(self, robot: urdfpy.URDF) -> None:
        self.robot: urdfpy.URDF = robot
        self.name: str = robot.name or "robot"
        self.links: dict[str, urdfpy.Link] = {link.name: link for link in robot.links}
        self.joints: dict[str, urdfpy.Joint] = {j.name: j for j in robot.joints}
        self.parent_joint_of_link: dict[str, urdfpy.Joint] = {j.child: j for j in robot.joints}

    def _link_path(self, link_name: str) -> str:
        pj: urdfpy.Joint | None = self.parent_joint_of_link.get(link_name)
        if pj is None:
            return f"{self.name}/{link_name}"
        return f"{self._joint_path(pj.name)}/{link_name}"

    def _joint_path(self, joint_name: str) -> str:
        j: urdfpy.Joint = self.joints[joint_name]
        return f"{self._link_path(j.parent)}/{joint_name}"

    def link_path(self, link: urdfpy.Link) -> str:
        return self._link_path(link.name)

    def joint_child_link(self, joint: urdfpy.Joint) -> urdfpy.Link:
        return self.links[joint.child]

    def joint_axis_world(self, joint: urdfpy.Joint) -> Sequence[float]:
        axis_local: npt.NDArray[np.float64] = np.asarray(joint.axis, dtype=float)
        transform_matrix: npt.NDArray[np.float64] = np.asarray(joint.origin) if joint.origin is not None else np.eye(4)
        rotation_matrix: npt.NDArray[np.float64] = transform_matrix[:3, :3]
        return (rotation_matrix @ axis_local).tolist()


async def animate_one_joint(robot_cls: str, joint_name: str) -> None:
    assets_dir: Path = await download_robot_assets(robot_cls)
    urdf_file: Path = next(assets_dir.glob("*.urdf"))

    _patch_mesh_loader(urdf_file)  # <── key fix
    urdf: urdfpy.URDF = urdfpy.URDF.load(urdf_file)  # now loads fine

    # Dump all joint information for debugging/inspection
    dump_joint_origins(urdf)

    tree: UrdfTree = UrdfTree(urdf)
    joint: urdfpy.Joint | None = tree.joints.get(joint_name)
    if joint is None:
        raise ValueError(f"Joint '{joint_name}' not found")

    link: urdfpy.Link = tree.joint_child_link(joint)
    entity_path: str = link_entity_path(urdf, link.name, urdf_file)  # <-- NEW: use correct path
    axis_world: Sequence[float] = tree.joint_axis_world(joint)

    logger.info("Animating %s\n   axis_world = %s", entity_path, axis_world)

    # Fixed transform from the parent-link frame to the child-link frame
    # when the joint angle is ZERO (i.e. the <origin> pose in the URDF):
    transform_fixed: npt.NDArray[np.float64] = joint.get_child_pose()  # 4×4 homogeneous matrix

    # The joint axis expressed in the *parent* link frame:
    axis_parent: npt.NDArray[np.float64] = axis_in_parent(joint)  # already defined helper

    rr.init(f"{robot_cls}-urdf-demo", spawn=True)
    rr.log_file_from_path(urdf_file, static=True)

    for step in range(1_000):
        rr.set_time_sequence("step", step)
        angle: float = math.sin(step * 0.02) * 0.8  # whatever profile you like

        # 4×4 rotation about the joint axis, in the parent frame:
        transform_dynamic: npt.NDArray[np.float64] = trimesh.transformations.rotation_matrix(
            angle, axis_parent, point=[0, 0, 0]
        )

        # Combine fixed + dynamic:
        transform_total: npt.NDArray[np.float64] = transform_fixed @ transform_dynamic  # parent ➜ child at this step

        # Extract translation and rotation components for new Transform3D API:
        translation: npt.NDArray[np.float64] = transform_total[:3, 3]  # (x, y, z) w.r.t. the parent link
        rotation: rr.RotationAxisAngle = rr.RotationAxisAngle(axis_parent, angle)

        rr.log(
            entity_path,
            rr.Transform3D(
                translation=translation.astype(np.float32),
                rotation=rotation,
                from_parent=True,  # stay in the joint's local frame
            ),
        )

        await asyncio.sleep(0.02)

    logger.info("Finished – close the viewer to exit.")
    await asyncio.Event().wait()


def main() -> None:
    ap: argparse.ArgumentParser = argparse.ArgumentParser()
    ap.add_argument("--robot", "-r", default="zbot")
    ap.add_argument("--joint", "-j", default="right_hip_yaw")
    args: argparse.Namespace = ap.parse_args()

    asyncio.run(animate_one_joint(args.robot, args.joint))


if __name__ == "__main__":
    colorlogging.configure()
    main()
