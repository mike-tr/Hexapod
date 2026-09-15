import socket, json, time
from Initialization.servo import Servo
from Initialization.pca9685 import PCA9685
from Initialization.adc import ADC
from Initialization.hexapodConfig import HexapodConfig
from Initialization.tripodgait import TripodGait

PORT = 9000
WATCHDOG = 0.5  # seconds without a packet -> stop

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))
sock.setblocking(False)

cmd = {"vx": 0.0, "vy": 0.0, "omega": 0.0}
last_rx = time.time()

robot = HexapodConfig()

while True:
    # drain the queue, keep only the newest packet
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
        cmd = {"vx": 0.0, "vy": 0.0, "omega": 0.0}

    #hexapod.set_velocity(cmd["vx"], cmd["vy"], cmd["omega"])
    #hexapod.gait_tick()
    time.sleep(1 / 50)