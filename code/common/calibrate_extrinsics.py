import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import cv2, numpy as np
from pathlib import Path
# from client.lib.floor_chess import camera_pose_from_cheker_board
from common.lib.floor_markers import camera_pose_from_marker
from common.camera_config import CameraProfile, load_profile, Extrinsics, save_extrinsics, EXTRINSICS
from common.paths import IMAGES

fc = camera_pose_from_marker

profile = load_profile("stream")
heights, tilts, ranges = [], [], []
for f in sorted(IMAGES.glob("tempground_*.jpg")):
    img = cv2.imread(str(f))
    print(f.name)
    if img is None:
        print(f"{f.name}: unreadable")
        continue
    res = camera_pose_from_marker(profile, img)
    if res is None:
        print(f"{f.name}: no marker found")
        continue
    for mid, h,t,d in res:
        heights.append(h)
        tilts.append(t)
        ranges.append(d)
        print(f"    id{mid}  h {h:6.1f}  tilt {t:5.2f}  range {d/10:5.1f} cm")

if heights:
    print(f"\nmean height {np.mean(heights):.1f} mm  (spread {np.ptp(heights):.1f})")
    print(f"mean tilt   {np.mean(tilts):.2f}°  (spread {np.ptp(tilts):.2f})")

ranges = np.array(ranges)
mean_weighted_height = np.average(heights, weights= 1.0 / ranges ** 4)
mean_weighted_tilt = np.average(tilts, weights= 1.0 / ranges ** 4)

if heights:
    print(f"\nmean weighted height {mean_weighted_height:.1f} mm")
    print(f"mean weighted tilt   {mean_weighted_tilt:.2f}°")

    save_extrinsics(Extrinsics(height_mm=mean_weighted_height, tilt_deg=mean_weighted_tilt, forward_mm=EXTRINSICS.forward_mm, right_mm=EXTRINSICS.right_mm))


# heights, tilts = [], []
# for f in sorted(IMAGES.glob("fchess2_*.jpg")):
#     img = cv2.imread(str(f))
#     print(f.name)
#     if img is None:
#         print(f"{f.name}: unreadable")
#         continue
#     r = camera_pose_from_cheker_board(img)
#     if r is None:
#         print(f"{f.name}: no marker found")
#         continue
#     h, t = r
#     heights.append(h)
#     tilts.append(t)
#     print(f"{f.name}: height {h:7.1f} mm   tilt {t:6.2f}°")

# if heights:
#     print(f"\nmean height {np.mean(heights):.1f} mm  (spread {np.ptp(heights):.1f})")
#     print(f"mean tilt   {np.mean(tilts):.2f}°  (spread {np.ptp(tilts):.2f})")