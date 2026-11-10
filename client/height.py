import cv2, numpy as np
from pathlib import Path
from initialization.floorFromMarker import camera_pose_from_marker
from initialization.floorFromCheckerBoard import camera_pose_from_cheker_board
from initialization.path import CALIB

fc = camera_pose_from_cheker_board

heights, tilts = [], []
for f in sorted(CALIB.glob("floor_*.jpg")):
    img = cv2.imread(str(f))
    if img is None:
        print(f"{f.name}: unreadable")
        continue
    r = fc(img)
    if r is None:
        print(f"{f.name}: no marker found")
        continue
    h, t, mid = r
    heights.append(h)
    tilts.append(t)
    print(f"{f.name}: id {mid}   height {h:7.1f} mm   tilt {t:6.2f}°")

if heights:
    print(f"\nmean height {np.mean(heights):.1f} mm  (spread {np.ptp(heights):.1f})")
    print(f"mean tilt   {np.mean(tilts):.2f}°  (spread {np.ptp(tilts):.2f})")