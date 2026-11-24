import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import cv2, glob, json
import numpy as np
from common.paths import IMAGES, CONFIG
from common.camera_config import CameraProfile, load_profile, save_profile


def calibrate_intrinsics(profile: CameraProfile, images, pattern, square_mm):
    objp = np.zeros((pattern[0] * pattern[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:pattern[0], 0:pattern[1]].T.reshape(-1, 2) * square_mm

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objpoints, imgpoints, used = [], [], []
    size = None


    for f in sorted(images):
        img = cv2.imread(str(f))
        if img is None:
            print(f"{f.name}: unreadable")
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        size = gray.shape[::-1]

        ok, corners = cv2.findChessboardCorners(
            gray, pattern,
            cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE)
        if not ok:
            print(f"{f.name}: no pattern")
            continue

        corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        objpoints.append(objp)
        imgpoints.append(corners)
        used.append(f.name)

    print(f"\nusing {len(used)} of {len(images)} images at {size}")
    if len(used) < 10:
        raise SystemExit("too few detections")

    rms, K, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, size, None, None, flags=cv2.CALIB_RATIONAL_MODEL)

    print(f"\noverall RMS: {rms:.4f} px\n")
    for i, name in enumerate(used):
        proj, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], K, dist)
        d = imgpoints[i].reshape(-1, 2) - proj.reshape(-1, 2)
        err = float(np.sqrt((d ** 2).sum(axis=1).mean()))
        flag = "  <-- outlier" if err > 1.8 * rms else ""
        print(f"  {err:.4f}  {name}{flag}")

    print("\nK =\n", K)
    print("\ndist =", dist.ravel())

    W, H = profile.capture.size
    allpts = np.concatenate([c.reshape(-1, 2) for c in imgpoints])
    frac_w = (allpts[:, 0].max() - allpts[:, 0].min()) / W
    frac_h = (allpts[:, 1].max() - allpts[:, 1].min()) / H
    print(f"coverage: frac_w {frac_w:.2f}  frac_h {frac_h:.2f}")

    save_profile(profile.with_intrinsics(K=K, dist=dist, rms_px=rms, n_images=len(images)))

def main():
    pattern   = (6, 9)                   # inner corners
    square_mm = 25


    CALIB_IMAGES = IMAGES
    NAME = "temp"

    images = sorted(CALIB_IMAGES.glob(f"{NAME}_*.jpg"))
    profile = load_profile("stream")

    calibrate_intrinsics(profile=profile, images=images, pattern=pattern, square_mm=square_mm)



    
if __name__ == "__main__":
    main()