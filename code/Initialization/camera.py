import socket, struct, cv2
from picamera2 import Picamera2
import numpy as np
from numpy.typing import NDArray
from libcamera import Transform
import threading

class CameraCapture:
    def __init__(self, resoltion):
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_video_configuration(
                main={"size": resoltion, "format": "RGB888"}, transform=Transform(hflip=1, vflip=1)))
        self.picam2.start()

    def get_frame(self) -> NDArray[np.uint8]:
        return self.picam2.capture_array()

CHUNK = 1400
HDR = struct.Struct("!IHH")       # frame_id, chunk_index, total_chunks

class FrameSender:
    def __init__(self, host = "0.0.0.0", port=9001, quality=80):
        self.addr = (host, port)
        self.quality = quality
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.frame_id = 0
        self.cam = CameraCapture((1280,720))
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)


    def start(self):
        self._thread.start()

    def _run(self):
        while not self._stop.is_set():
            self.send(self.cam.get_frame())

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


class FrameReceiver:
    def __init__(self, post_processing, host = "0.0.0.0", port=9001, max_pending=8):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1 << 22)
        self.sock.bind((host, port))
        self.pending = {}
        self.post_processing = post_processing
        self.max_pending = max_pending
        self.lastframe = -1
        self.frame: NDArray[np.uint8] | None = None
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        self._thread.start()

    def _run(self):
        while not self._stop.is_set():
            self.frame = self.recv()
        print("camera down")

    def stop(self):
        self._stop.set()
        self._thread.join(timeout=2.0)
        

    def recv(self) -> NDArray[np.uint8] | None:
        """Block until a complete frame arrives, then return it."""
        while not self._stop.is_set():
            pkt, _ = self.sock.recvfrom(2048)
            fid, idx, total = HDR.unpack_from(pkt)
            if fid <= self.lastframe:
                continue

            chunks = self.pending.setdefault(fid, {})
            chunks[idx] = pkt[HDR.size:]

            if len(chunks) == total:
                data = b"".join(chunks[i] for i in range(total))
                for id in list(self.pending.keys()):
                    if id <= self.lastframe:
                        del self.pending[id]
                #del self.pending[fid]
                img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
                if img is not None:
                    return self.post_processing(img)

            if len(self.pending) > self.max_pending:
                oldest = min(self.pending)
                del self.pending[oldest]