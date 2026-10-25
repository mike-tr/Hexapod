import socket, struct, cv2
import numpy as np
from numpy.typing import NDArray
import threading

CHUNK = 1400
HDR = struct.Struct("!IHH")       # frame_id, chunk_index, total_chunks

class FrameReceiver:
    def __init__(self, host = "0.0.0.0", port=9001, max_pending=8):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1 << 22)
        print((host, port))
        self.sock.bind((host, port))
        self.pending = {}
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
                #print(data)
                for id in list(self.pending.keys()):
                    if id <= self.lastframe:
                        del self.pending[id]
                #del self.pending[fid]
                img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
                if img is not None:
                    return img

            if len(self.pending) > self.max_pending:
                oldest = min(self.pending)
                del self.pending[oldest]