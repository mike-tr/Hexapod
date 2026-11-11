import cv2, numpy as np
from pathlib import Path
from client.lib.floor_chess import camera_pose_from_marker
from client.lib.floor_markers import camera_pose_from_cheker_board
from common.paths import IMAGES

fc = camera_pose_from_cheker_board

heights, tilts = [], []
for f in sorted(IMAGES.glob("marker_*.jpg")):
    img = cv2.imread(str(f))
    print(f.name)
    if img is None:
        print(f"{f.name}: unreadable")
        continue
    res = camera_pose_from_marker(img)
    if res is None:
        print(f"{f.name}: no marker found")
        continue
    for mid, h,t,d in res:
        heights.append(h)
        tilts.append(t)
        print(f"    id{mid}  h {h:6.1f}  tilt {t:5.2f}  range {d/10:5.1f} cm")

if heights:
    print(f"\nmean height {np.mean(heights):.1f} mm  (spread {np.ptp(heights):.1f})")
    print(f"mean tilt   {np.mean(tilts):.2f}°  (spread {np.ptp(tilts):.2f})")


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