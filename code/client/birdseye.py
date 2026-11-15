import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import cv2, glob, json
import numpy as np
from common.vector import Vec3
from common.paths import IMAGES
from common.camera_calibration import K, DIST, EXTRINSICS

# d = np.load(CALIB / "camera_calib.npz")
img = cv2.imread(IMAGES / "birdseye_00.jpg")

HEIGHT_MM = 86.0 #mm
TILT_DEG = 1.0
CAM_FWD_MM = 84.0 

R0 = np.array([[1., 0., 0.],      # cam +x (right)   = body +x
               [0., 0., -1.],     # cam +y (down)    = body -z
               [0., 1., 0.]])     # cam +z (forward) = body +y


# cv2.imshow("before", img)
# cv2.imshow("after", cv2.undistort(img, K, DIST))
# cv2.waitKey(0)

def _cam_from_body(tilt_deg: float) -> np.ndarray:
    th = np.radians(tilt_deg)
    c, s = np.cos(th), np.sin(th)
    Rx = np.array([[1., 0., 0.],
                   [0.,  c, -s],
                   [0.,  s,  c]])
    R = Rx @ R0
    assert np.isclose(np.linalg.det(R), 1.0)    # rotation, not a reflection
    return R

def local_robot_point_to_pixel(pos : Vec3) -> (float | float):
    camera_position = Vec3(0, EXTRINSICS.forward_mm, EXTRINSICS.height_mm)
    camera_frame_pos  = Vec3(*pos) - camera_position

    R = _cam_from_body(EXTRINSICS.tilt_deg)

    uvw = (K @ R @ camera_frame_pos)
    return (uvw / uvw[2])[:-1]


print(local_robot_point_to_pixel((0, 500, 0)))

# import numpy as np, cv2

# d = np.load("calibration/camera_calib.npz")
# K, dist = d["K"], d["dist"]
# w, h = 1280, 720

# pts = np.array([[[0, 0]], [[w-1, 0]], [[0, h-1]], [[w-1, h-1]],
#                 [[w//2, 0]], [[0, h//2]]], np.float32)
# und = cv2.undistortPoints(pts, K, dist, P=K)

# for p, u in zip(pts.reshape(-1, 2), und.reshape(-1, 2)):
#     print(f"({p[0]:6.0f},{p[1]:6.0f}) -> ({u[0]:7.1f},{u[1]:7.1f})   shift {np.linalg.norm(p-u):5.2f} px")