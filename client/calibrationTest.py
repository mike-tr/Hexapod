import cv2, glob, json
import numpy as np
from pathlib import Path
from Initialization.path import CALIB

CALIB_IMAGES = CALIB / "images" 

d = np.load(CALIB / "camera_calib.npz")
img = cv2.imread(CALIB_IMAGES / "test_00.jpg")
cv2.imshow("before", img)
cv2.imshow("after", cv2.undistort(img, d["K"], d["dist"]))
cv2.waitKey(0)