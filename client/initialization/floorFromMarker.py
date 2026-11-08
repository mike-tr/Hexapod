import cv2, numpy as np
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from path import CALIB

d = np.load(CALIB / "camera_calib.npz")
K, dist = d["K"], d["dist"]

MARKER_MM = 140.3          # measure your printed black square
half = MARKER_MM / 2
objp = np.array([[-half,  half, 0],
                 [ half,  half, 0],
                 [ half, -half, 0],
                 [-half, -half, 0]], np.float32)

adict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
detector = cv2.aruco.ArucoDetector(adict, cv2.aruco.DetectorParameters())



def camera_pose_from_marker(frame):
    corners, ids, _ = detector.detectMarkers(frame)
    if ids is None:
        return None

    _, rvec, tvec = cv2.solvePnP(objp, corners[0][0], K, dist,
                                 flags=cv2.SOLVEPNP_IPPE_SQUARE)

    R, _ = cv2.Rodrigues(rvec)        # 3x3, marker frame -> camera frame
    R_cam = R.T                       # camera orientation in marker frame
    cam_pos = (-R_cam @ tvec).ravel() # camera position in marker frame

    height = float(cam_pos[2])        # marker lies on the floor, so this is
                                      # the camera's height above it

    # where the optical axis points, relative to the floor
    axis = R_cam @ np.array([0.0, 0.0, 1.0])
    tilt = float(np.degrees(np.arcsin(-axis[2])))

    return height, tilt, int(ids.ravel()[0])