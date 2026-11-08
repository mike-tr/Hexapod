import cv2, numpy as np
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from path import CALIB

d = np.load(CALIB / "camera_calib.npz")
print(d)
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