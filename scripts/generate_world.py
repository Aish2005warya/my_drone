#!/usr/bin/env python3
"""
Strips the second drone (X4) out of Gazebo's stock
multicopter_velocity_control.sdf world, leaving only the X3 quadcopter.
"""
import os
import xml.etree.ElementTree as ET
import glob

PACKAGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(PACKAGE_DIR, "worlds", "one_drone.sdf")


def find_source_world():
    search_roots = ["/opt/ros", "/usr/share"]
    for root in search_roots:
        matches = glob.glob(
            os.path.join(root, "**", "multicopter_velocity_control.sdf"),
            recursive=True,
        )
        if matches:
            return matches[0]
    raise FileNotFoundError(
        "Could not find multicopter_velocity_control.sdf under /opt/ros or "
        "/usr/share. Make sure ros-<distro>-ros-gz is installed."
    )


def strip_second_drone(src_path, dst_path, drone_to_remove="x4"):
    tree = ET.parse(src_path)
    world = tree.getroot().find("world")
    if world is None:
        raise RuntimeError(f"No <world> element found in {src_path}")

    removed = []
    for el in list(world):
        if el.tag not in ("model", "include"):
            continue
        name = (el.get("name") or el.findtext("name") or "").lower()
        uri = (el.findtext("uri") or "").lower()
        if name == drone_to_remove or drone_to_remove in uri:
            world.remove(el)
            removed.append(f"{el.tag}:{name or uri}")

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    tree.write(dst_path)
    return removed


if __name__ == "__main__":
    src = find_source_world()
    print(f"Source world: {src}")
    removed = strip_second_drone(src, OUTPUT_PATH)
    print(f"Removed {len(removed)} element(s): {removed}")
    print(f"Wrote: {OUTPUT_PATH}")
