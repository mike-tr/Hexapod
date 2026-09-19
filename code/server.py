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
tripod = TripodGait(2, 40)
tripod.load_gait(TripodGait.TRIPLE_GAIT)


prev = time.monotonic()
DT = 0.02
SPEED = 1.1
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
    dt = time.monotonic() - prev
    prev = time.monotonic()
    print(cmd)
    # if abs(cmd["vx"]) > 0:
    #     tripod.update(dt * SPEED, robot.legs, 50 * cmd["vx"])


    if abs(cmd["vx"]) > 0 or abs(cmd["vy"]) > 0 or abs(cmd["omega"]) > 0:
        tripod.update(dt * SPEED, robot.legs, 50 * cmd["vx"], 50 * cmd["vy"], cmd["omega"] * 15)
    # if current_command == "w":
    #     tripod.update(dt * SPEED, robot.legs, 50)
    #     time.sleep(DT)
    # elif current_command == "s":
    #     tripod.update(dt * SPEED, robot.legs, -50)
    # else:
    #     robot.home()
    time.sleep(1 / 50)