import cv2, numpy as np
import sys, os

print("test")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from path import CALIB

print("test", CALIB / "camera_calib.npz")
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


def annotate(frame):
    corners, ids, _ = detector.detectMarkers(frame)
    if ids is None:
        return frame

    cv2.aruco.drawDetectedMarkers(frame, corners, ids)
    for c, mid in zip(corners, ids.ravel()):
        ok, rvec, tvec = cv2.solvePnP(objp, c[0], K, dist,
                                      flags=cv2.SOLVEPNP_IPPE_SQUARE)
        if not ok:
            continue
        cv2.drawFrameAxes(frame, K, dist, rvec, tvec, MARKER_MM / 2)
        dmm = float(np.linalg.norm(tvec))
        x, y = c[0][0]
        cv2.putText(frame, f"id{mid}  {dmm/10:.1f} cm", (int(x), int(y) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        x, y, z = tvec.ravel()
        print(f"x {x/10:.1f}  y {y/10:.1f}  z {z/10:.1f}  |d| {np.linalg.norm(tvec)/10:.1f} cm")
    return frame

PATTERN = (6, 9)
SQUARE_MM = 23.5 
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objpc = np.zeros((PATTERN[0] * PATTERN[1], 3), np.float32)
objpc[:, :2] = np.mgrid[0:PATTERN[0], 0:PATTERN[1]].T.reshape(-1, 2) * SQUARE_MM


def annotate_cheker(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ok, corners = cv2.findChessboardCorners(
        gray, PATTERN,
        cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE)
    if not ok:
        return frame

    corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

    ok, rvec, tvec = cv2.solvePnP(objpc, corners, K, dist)
    if not ok:
        return frame

    w = (PATTERN[0] - 1) * SQUARE_MM
    h = (PATTERN[1] - 1) * SQUARE_MM
    d = 60.0                                   # box height, mm

    box = np.float32([
        [0,0,0], [w,0,0], [w,h,0], [0,h,0],           # base, on the board
        [0,0,-d], [w,0,-d], [w,h,-d], [0,h,-d],       # top
    ])
    pts, _ = cv2.projectPoints(box, rvec, tvec, K, dist)
    pts = pts.reshape(-1, 2).astype(np.int32)

    cv2.drawContours(frame, [pts[:4]], -1, (0, 255, 0), 2)        # base
    for i in range(4):
        cv2.line(frame, tuple(pts[i]), tuple(pts[i+4]), (255, 0, 0), 2)
    cv2.drawContours(frame, [pts[4:]], -1, (0, 0, 255), 2)        # top
    for i in range(4):
        cv2.line(frame, tuple(pts[i]), tuple(pts[i+4]), (255, 0, 0), 2)
    cv2.drawContours(frame, [pts[4:]], -1, (0, 0, 255), 2)

    cv2.drawFrameAxes(frame, K, dist, rvec, tvec, 50)

    # r = camera_pose_from_cheker_board(frame)
    # if r:
    #     height, tilt = r
    #     cv2.putText(frame, f"h {height:.0f} mm   tilt {tilt:.1f}deg",
    #                 (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    return frame