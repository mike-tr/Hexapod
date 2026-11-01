import picamera2, cv2
print(cv2.__version__, hasattr(cv2, "aruco"))
import time
from Initialization.camera import FrameSender

sender = FrameSender()
import threading, atexit

stop = threading.Event()

def main():
    sender.start()
    try:
        while not stop.is_set():
            print("sending...")
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