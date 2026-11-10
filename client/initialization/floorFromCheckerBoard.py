import cv2, numpy as np
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from path import CALIB

d = np.load(CALIB / "camera_calib.npz")

K, dist = d["K"], d["dist"]

PATTERN = (6, 9)
SQUARE_MM = 23.5          # MEASURE THIS for the board you're using

objp = np.zeros((PATTERN[0] * PATTERN[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:PATTERN[0], 0:PATTERN[1]].T.reshape(-1, 2) * SQUARE_MM

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


def camera_pose_from_cheker_board(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ok, corners = cv2.findChessboardCorners(
        gray, PATTERN,
        cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE)
    if not ok:
        return None

    corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

    ok, rvec, tvec = cv2.solvePnP(objp, corners, K, dist)
    if not ok:
        return None

    R, _ = cv2.Rodrigues(rvec)        # board frame -> camera frame
    R_cam = R.T                       # camera orientation in board frame
    cam_pos = (-R_cam @ tvec).ravel() # camera position in board frame

    # board z may point into the floor; normalise so height is positive
    flip = -1.0 if cam_pos[2] < 0 else 1.0

    height = flip * float(cam_pos[2])

    axis = R_cam @ np.array([0.0, 0.0, 1.0])
    tilt = float(np.degrees(np.arcsin(np.clip(-flip * axis[2], -1.0, 1.0))))

    return height, tilt