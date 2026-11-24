import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import cv2, glob, json
import numpy as np
from pathlib import Path
from common.paths import IMAGES
from common.camera_config import CameraProfile, load_profile

def show(name, img, scale=0.5):
    small = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    cv2.imshow(name, small)

CALIB_IMAGES = IMAGES 

profile = load_profile("stream")

img = cv2.imread(CALIB_IMAGES / "temp_00.jpg")
show("before", img)
show("after", cv2.undistort(img, profile.intrinsics.K, profile.intrinsics.dist))
# cv2.imshow("before", img)
# cv2.imshow("after", cv2.undistort(img, profile.intrinsics.K, profile.intrinsics.dist))
cv2.waitKey(0)

import numpy as np, cv2
w, h = 2304, 1296

pts = np.array([[[0, 0]], [[w-1, 0]], [[0, h-1]], [[w-1, h-1]],
                [[w//2, 0]], [[0, h//2]]], np.float32)
und = cv2.undistortPoints(pts, profile.intrinsics.K, profile.intrinsics.dist, P=profile.intrinsics.K)

for p, u in zip(pts.reshape(-1, 2), und.reshape(-1, 2)):
    print(f"({p[0]:6.0f},{p[1]:6.0f}) -> ({u[0]:7.1f},{u[1]:7.1f})   shift {np.linalg.norm(p-u):5.2f} px")

d = np.asarray(profile.intrinsics.dist).ravel()
print(f"dist has {d.size} coefficients")

k1, k2, p1, p2 = d[0], d[1], d[2], d[3]
k3 = d[4] if d.size > 4 else 0.0
k4, k5, k6 = (d[5], d[6], d[7]) if d.size >= 8 else (0.0, 0.0, 0.0)

for r in np.arange(0, 2.0, 0.1):
    r2 = r * r
    num = 1 + k1*r2 + k2*r2**2 + k3*r2**3
    den = 1 + k4*r2 + k5*r2**2 + k6*r2**3
    print(f"r={r:4.1f}  r_dist={r*num/den:7.4f}")