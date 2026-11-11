import cv2, glob, json
import numpy as np
from pathlib import Path
from common.paths import IMAGES
from common.camera_calibration import K, DIST

# d = np.load(CALIB / "camera_calib.npz")
img = cv2.imread(IMAGES / "birdseye_00.jpg")

HEIGHT_MM = 86.0 #mm
TILT_DEG = 1.0
CAM_FWD_MM = 84.0 

cv2.imshow("before", img)
cv2.imshow("after", cv2.undistort(img, d["K"], d["dist"]))
cv2.waitKey(0)

def local_point_to_pixel(x, y, z) -> (float | float):
    pass

# import numpy as np, cv2

# d = np.load("calibration/camera_calib.npz")
# K, dist = d["K"], d["dist"]
# w, h = 1280, 720

# pts = np.array([[[0, 0]], [[w-1, 0]], [[0, h-1]], [[w-1, h-1]],
#                 [[w//2, 0]], [[0, h//2]]], np.float32)
# und = cv2.undistortPoints(pts, K, dist, P=K)

# for p, u in zip(pts.reshape(-1, 2), und.reshape(-1, 2)):
#     print(f"({p[0]:6.0f},{p[1]:6.0f}) -> ({u[0]:7.1f},{u[1]:7.1f})   shift {np.linalg.norm(p-u):5.2f} px")