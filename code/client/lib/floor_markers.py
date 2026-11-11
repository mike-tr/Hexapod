import cv2, numpy as np
from common.camera_calibration import K, DIST

# d = np.load(CALIB / "camera_calib.npz")
# K, DIST = d["K"], d["DIST"]

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

    out = []
    for c, mid in zip(corners, ids.ravel()):
        ok, rvec, tvec = cv2.solvePnP(objp, c[0], K, DIST,
                                      flags=cv2.SOLVEPNP_IPPE_SQUARE)
        if not ok:
            continue
        R, _ = cv2.Rodrigues(rvec)
        R_cam = R.T
        cam_pos = (-R_cam @ tvec).ravel()
        flip = -1.0 if cam_pos[2] < 0 else 1.0
        height = flip * float(cam_pos[2])
        axis = R_cam @ np.array([0.0, 0.0, 1.0])
        tilt = float(np.degrees(np.arcsin(np.clip(-flip*axis[2], -1, 1))))
        out.append((int(mid), height, tilt, float(np.linalg.norm(tvec))))

    return out