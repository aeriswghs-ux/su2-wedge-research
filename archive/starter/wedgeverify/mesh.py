"""Generate structured quadrilateral 2-D SU2 wedge-in-channel meshes.

Coordinates in metres. Exterior marker orientations are consistent with
counterclockwise interior cells. Mesh files are generated, not SU2-tested.
"""
from pathlib import Path
from math import tan, radians
import argparse

GRID_LEVELS = {"coarse": (60, 40), "medium": (120, 80), "fine": (240, 160)}


def bottom_y(x: float, tip_x: float = 0.5, theta_deg: float = 10.0) -> float:
    return max(0.0, x - tip_x) * tan(radians(theta_deg))


def generate_mesh(path: str | Path, nx: int, ny: int,
                  length: float = 1.5, height: float = 1.0,
                  tip_x: float = 0.5, theta_deg: float = 10.0):
    if nx < 2 or ny < 2 or length <= 0 or height <= 0 or not 0 < tip_x < length:
        raise ValueError("Invalid mesh dimensions")
    if nx * tip_x / length != round(nx * tip_x / length):
        raise ValueError("The tip x coordinate must fall on a mesh vertex")
    if bottom_y(length, tip_x, theta_deg) >= height:
        raise ValueError("Wedge intersects the upper boundary")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    idx = lambda i, j: j * (nx + 1) + i
    with path.open("w", encoding="utf-8") as f:
        f.write("NDIME= 2\n")
        f.write(f"NELEM= {nx*ny}\n")
        for j in range(ny):
            for i in range(nx):
                f.write(f"9 {idx(i,j)} {idx(i+1,j)} {idx(i+1,j+1)} {idx(i,j+1)}\n")
        f.write(f"NPOIN= {(nx+1)*(ny+1)}\n")
        for j in range(ny+1):
            fraction = j / ny
            for i in range(nx+1):
                x = length * i / nx
                y = bottom_y(x, tip_x, theta_deg)
                y += fraction * (height-y)
                f.write(f"{x:.13g} {y:.13g} {idx(i,j)}\n")
        groups = {
            "lower": [(idx(i,0), idx(i+1,0)) for i in range(nx)],
            "upper": [(idx(i+1,ny), idx(i,ny)) for i in range(nx)],
            "inlet": [(idx(0,j+1), idx(0,j)) for j in range(ny)],
            "outlet": [(idx(nx,j), idx(nx,j+1)) for j in range(ny)],
        }
        f.write("NMARK= 4\n")
        for marker, edges in groups.items():
            f.write(f"MARKER_TAG= {marker}\nMARKER_ELEMS= {len(edges)}\n")
            for a, b in edges:
                f.write(f"3 {a} {b}\n")
    return {"name": path.name, "cells": nx*ny, "points": (nx+1)*(ny+1),
            "nx": nx, "ny": ny, "tip_x_m": tip_x, "length_m": length,
            "height_m": height, "theta_deg": theta_deg,
            "nominal_h_m": ((length*height - 0.5*(length-tip_x)**2*tan(radians(theta_deg)))/(nx*ny)) ** 0.5}


def main():
    parser = argparse.ArgumentParser(description="Generate the three SU2 wedge meshes")
    parser.add_argument("--out-dir", default="meshes")
    args = parser.parse_args()
    for level, (nx, ny) in GRID_LEVELS.items():
        metadata = generate_mesh(Path(args.out_dir) / f"wedge_{level}.su2", nx, ny)
        print(f"{level}: {metadata['cells']:,} quads, {metadata['points']:,} nodes")

if __name__ == "__main__":
    main()
