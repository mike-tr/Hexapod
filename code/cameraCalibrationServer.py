import picamera2, cv2
import socket, json
print(cv2.__version__, hasattr(cv2, "aruco"))
import time
from Initialization.camera import FrameSender,CameraCapture

camera =  CameraCapture((1280,720))
sender = FrameSender(camera, "192.168.10.19")

PORT = 9000
WATCHDOG = 0.5  # seconds without a packet -> stop

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))
sock.setblocking(False)

import threading, atexit

stop = threading.Event()


def cpu_temp() -> float:
    with open("/sys/class/thermal/thermal_zone0/temp") as f:
        return int(f.read()) / 1000.0


def main():
    last_rx = time.time()
    sender.start()
    cmd_initial = {"lx": 0.0, "ly": 0.0, "rx": 0.0, "ry" : 0.0, "hx": 0.0, "hy": 0.0, "rt": -1.0, "shoot": False}
    cmd = cmd_initial.copy()
    id = 0
    try:
        while not stop.is_set():
            while True:
                try:
                    data, _ = sock.recvfrom(1024)
                except BlockingIOError:
                    break
                try:
                    cmd = json.loads(data)
                    last_rx = time.time()
                except json.JSONDecodeError:
                    pass
            if time.time() - last_rx > WATCHDOG:
                cmd = cmd_initial.copy()


            if cmd["shoot"]:
                camera.save_frame("test", id)
                id += 1

            print(cmd)
            time.sleep(1 / 50)

    except KeyboardInterrupt:
        pass
    finally:
        stop.set()

if __name__ == "__main__":
    main()
