import picamera2, cv2
print(cv2.__version__, hasattr(cv2, "aruco"))
import time
from Initialization.camera import FrameSender

sender = FrameSender("192.168.10.19")
import threading, atexit

stop = threading.Event()


def cpu_temp() -> float:
    with open("/sys/class/thermal/thermal_zone0/temp") as f:
        return int(f.read()) / 1000.0


def main():
    sender.start()
    try:
        while not stop.is_set():
            print(f"{cpu_temp():.1f} °C")
            time.sleep(1)
            pass
    except KeyboardInterrupt:
        pass
    finally:
        stop.set()

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()