import cv2
print(cv2.__version__, hasattr(cv2, "aruco"))
import time, socket
from cameraClient import FrameReceiver

reciever = FrameReceiver()
import threading, atexit

stop = threading.Event()


ROBOT = ("192.168.10.21", 9000)   # your Pi's IP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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