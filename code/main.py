from Initialization.servo import Servo
from Initialization.pca9685 import PCA9685
from Initialization.adc import ADC
from Initialization.hexapod import Hexapod
from Initialization.tripodgait import TripodGait
import time
import threading
from sshkeyboard import listen_keyboard, stop_listening


# current_command = {}
# for key in ["w","a","s","d"]:
#     current_command[key] = False

robot = Hexapod()

robot.home()
time.sleep(1)


current_command = "none"
running = True
def keyboard_listener_worker():
    """This function runs inside its own thread to handle SSH key events."""
    global current_command, running

    def press(key):
        global current_command
        if key in ["w", "a", "s", "d", "space"]:
            current_command = key
            robot.tripod.reset()
        elif key == "q":
            print("\nShutting down listener...")
            stop_listening()

    def release(key):
        global current_command
        # Optional: Stop walking when the key is released
        if key == current_command:
            current_command = "none"

    # Start the blocking listener loop inside this thread
    listen_keyboard(on_press=press, on_release=release, sequential=True)
    running = False  # Signal main thread that we are exiting


listener_thread = threading.Thread(target=keyboard_listener_worker, daemon=True)
listener_thread.start()

prev = time.monotonic()
DT = 0.02
SPEED = 1.1
while running:
    dt = time.monotonic() - prev
    prev = time.monotonic()
    if current_command == "w":
        #robot.tripod.update(dt * SPEED, robot.legs, 0, 50, 0)
        robot.tripod.update(dt * SPEED, robot.legs, 0, 0, 10)
        time.sleep(DT)
    elif current_command == "s":
        #robot.tripod.update(dt * SPEED, robot.legs, 0, -50 ,0)
        robot.tripod.update(dt * SPEED, robot.legs, 0, 0, -10)
    else:
        robot.home()

robot.relax()
