# Hexapod Robot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A custom-designed 6-legged robot built from scratch, featuring 3D-printed parts, MG996R servos, and a Raspberry Pi 5 running ROS2.

## Status

**Work in progress** — 3 legs assembled, 3 more printing. Next steps: complete assembly, wire PCB + Raspberry Pi, then software.

- [x] CAD design (legs, chassis, battery holder)
- [x] STL exports
- [x] 3 legs assembled
- [ ] Full 6-leg assembly
- [ ] PCB + Raspberry Pi integration
- [ ] ROS2 firmware & gait control

## Assembly Preview

<p float="left">
  <img src="media/WhatsApp Image 2026-05-30 at 14.24.14.jpeg" width="32%" />
  <img src="media/WhatsApp Image 2026-05-30 at 14.24.15.jpeg" width="32%" />
</p>

## Hardware

| Component | Details |
|---|---|
| Brain | Raspberry Pi 5 |
| Servos | MG996R × 18 (3 per leg) |
| PCB | Freenove Big Hexapod Robot PCB (reused) |
| Battery | 18500 flat cells |
| Frame | Custom 3D-printed (FreeCAD) |

## 3D Printed Parts

All STL files are in [cad/stl/](cad/stl/). Source FreeCAD files are in [cad/freecad/](cad/freecad/).

**Leg** (× 6):
- `coxa_mount.stl`
- `coxa_vertical.stl`
- `coxa_horizontal.stl`
- `femur_mount1.stl`
- `femur_mount2.stl`
- `tibia_mount.stl`
- `tibia.stl`
- `foot.stl`

**Body:**
- `chassis.stl`
- `battery_holder.stl`

Each leg has 3 degrees of freedom (coxa / femur / tibia joints), driven by one MG996R servo each.

## Planned Software Stack

- **OS:** Raspberry Pi OS
- **Framework:** ROS2
- Inverse kinematics node
- Gait controller (tripod, wave)
- Teleop interface

## Roadmap

1. Complete 6-leg mechanical assembly
2. Mount PCB and Raspberry Pi 5 to chassis
3. Wire all 18 servos to PCB
4. Bring up ROS2 environment on Raspberry Pi 5
5. Implement IK solver and basic gaits (tripod, wave)
6. Add sensors / teleoperation
