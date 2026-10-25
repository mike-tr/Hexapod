import cv2
print(cv2.__version__, hasattr(cv2, "aruco"))
import time
from cameraClient import FrameReceiver

reciever = FrameReceiver()
import threading, atexit

stop = threading.Event()


def main():
    reciever.start()
    try:
        while not stop.is_set():
            frame = reciever.frame
            if frame is not None:
                cv2.imshow("hexapod", frame)
                if cv2.waitKey(16) == 27:        # 27 = Escape
                    break
            pass
    except KeyboardInterrupt:
        pass
    finally:
        stop.set()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()