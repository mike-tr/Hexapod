import socket, struct, cv2
import numpy as np
from numpy.typing import NDArray
import threading, sys, os
from collections.abc import Callable
from typing import Literal
from common.camera_calibration import CameraProfile


CHUNK = 1400
HDR = struct.Struct("!IHH")       # frame_id, chunk_index, total_chunks

class FrameSender:
    def __init__(self, source: Callable[[], NDArray[np.uint8]], host = "0.0.0.0", port=9001, quality=80):
        self.addr = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.quality = quality
        self.frame_id = 0
        self.source = source
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)


    def start(self):
        self._thread.start()

    def _run(self):
        while not self._stop.is_set():
            self.send(self.source())
        print("camera down")

    def stop(self):
        self._stop.set()
        self._thread.join(timeout=2.0)

    def send(self, frame: NDArray[np.uint8]):
        ok, enc = cv2.imencode(".jpg", frame,
                               [cv2.IMWRITE_JPEG_QUALITY, self.quality])
        if not ok:
            return
        data = enc.tobytes()
        total = ((len(data) - 1) // CHUNK) + 1
        for i in range(total):
            part = data[i * CHUNK : (i + 1) * CHUNK]
            self.sock.sendto(HDR.pack(self.frame_id, i, total) + part, self.addr)
        self.frame_id = (self.frame_id + 1) % (2**32)