import cv2, glob, json
import numpy as np
from pathlib import Path
from initialization.path import CALIB

PATTERN   = (6, 9)                   # inner corners
SQUARE_MM = 23.5

CALIB_IMAGES = CALIB / "images" 

print(CALIB_IMAGES)

objp = np.zeros((PATTERN[0] * PATTERN[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:PATTERN[0], 0:PATTERN[1]].T.reshape(-1, 2) * SQUARE_MM

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objpoints, imgpoints, used = [], [], []
size = None

for f in sorted(CALIB_IMAGES.glob("test_*.jpg")):
    img = cv2.imread(str(f))
    if img is None:
        print(f"{f.name}: unreadable")
        continue
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    size = gray.shape[::-1]

    ok, corners = cv2.findChessboardCorners(
        gray, PATTERN,
        cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE)
    if not ok:
        print(f"{f.name}: no pattern")
        continue

    corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
    objpoints.append(objp)
    imgpoints.append(corners)
    used.append(f.name)

print(f"\nusing {len(used)} of 28 images at {size}")
if len(used) < 10:
    raise SystemExit("too few detections")

rms, K, dist, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, size, None, None)

print(f"\noverall RMS: {rms:.4f} px\n")
for i, name in enumerate(used):
    proj, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], K, dist)
    d = imgpoints[i].reshape(-1, 2) - proj.reshape(-1, 2)
    err = float(np.sqrt((d ** 2).sum(axis=1).mean()))
    flag = "  <-- outlier" if err > 1.8 * rms else ""
    print(f"  {err:.4f}  {name}{flag}")

print("\nK =\n", K)
print("\ndist =", dist.ravel())

np.savez(CALIB / "camera_calib.npz",
         K=K, dist=dist, rms=rms, size=size, square_mm=SQUARE_MM)

json.dump({
    "width": int(size[0]), "height": int(size[1]),
    "fx": float(K[0, 0]), "fy": float(K[1, 1]),
    "cx": float(K[0, 2]), "cy": float(K[1, 2]),
    "dist": [float(d) for d in dist.ravel()],
    "rms_px": float(rms),
    "square_mm": SQUARE_MM,
    "n_images": len(used),
}, open(CALIB / "camera_calib.json", "w"), indent=2)

print(f"\nsaved to {CALIB}")