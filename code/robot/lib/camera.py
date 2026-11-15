import socket, struct, cv2
from picamera2 import Picamera2
import numpy as np
from numpy.typing import NDArray
from libcamera import Transform, controls
import threading, sys, os
import time
from collections.abc import Callable
from typing import Literal
from common.camera_calibration import CameraProfile


from common.paths import IMAGES
IMAGES.mkdir(exist_ok=True)

class CameraCapture:
    def __init__(self, profile : CameraProfile):
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_video_configuration(
            main={"size": profile.capture.size, "format": profile.capture.format},
            lores={"size": profile.capture.lores, "format": profile.capture.format_lores},
            raw={"size": profile.capture.raw_size},
            transform=Transform(hflip=profile.capture.hflip, vflip=profile.capture.vflip),
        ))
        self.picam2.start()

    def get_full(self) -> NDArray[np.uint8]:
        """Full-resolution BGR frame. For measurement."""
        return self.picam2.capture_array("main")

    def get_preview(self) -> NDArray[np.uint8]:
        """Full-resolution BGR frame. For measurement."""
        return self.picam2.capture_array("lores")

    def save_frame(self, name, id):
        cv2.imwrite(str(IMAGES / f"{name}_{id:02d}.jpg" ), self.picam2.capture_array("main"), [cv2.IMWRITE_JPEG_QUALITY, 95])
        print("saved:", f"{name}_{id:02d}.jpg")

    def measure_and_lock(self, lens_position=1.5, settle=2.5):
        """Let auto-exposure and AWB converge, then freeze what they chose."""
        self.picam2.set_controls({
            "AeEnable": True,
            "AwbEnable": True,
            "AfMode": controls.AfModeEnum.Manual,
            "LensPosition": lens_position,
            "Sharpness": 0.0,
        })
        time.sleep(settle)

        md = self.picam2.capture_metadata()
        locked = {
            "ExposureTime": int(md["ExposureTime"]),
            "AnalogueGain": float(md["AnalogueGain"]),
            "ColourGains": tuple(float(g) for g in md["ColourGains"]),
            "LensPosition": lens_position,
            "Sharpness": 0.0,
        }

        self.picam2.set_controls({
            "AeEnable": False,
            "AwbEnable": False,
            **locked,
        })
        time.sleep(0.5)
        return locked

