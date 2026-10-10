import socket, json, time
from Initialization.servo import Servo
from Initialization.pca9685 import PCA9685
from Initialization.adc import ADC
from Initialization.hexapod import Hexapod
from Initialization.tripodgait import TripodGait
from Initialization.vector import Vec3
from Initialization.hexapodBrain import HexapodBrain

PORT = 9000
WATCHDOG = 0.5  # seconds without a packet -> stop

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))
sock.setblocking(False)

cmd = {"lx": 0.0, "ly": 0.0, "rx": 0.0, "ry" : 0.0, "hx": 0.0, "hy": 0.0, "rt": -1.0}
last_rx = time.time()

robot = Hexapod()
brain = HexapodBrain(robot)

prev = time.monotonic()
counter = 0
DT = 0.02
SPEED = 1.1
Strength = 20
Angle = 5
Height = 0

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
        cmd = {"lx": 0.0, "ly": 0.0, "rx": 0.0, "ry" : 0.0, "hx": 0.0, "hy": 0.0, "rt": -1.0}

    #hexapod.set_velocity(cmd["vx"], cmd["vy"], cmd["omega"])
    #hexapod.gait_tick()
    dt = time.monotonic() - prev
    prev = time.monotonic()
    
    # if abs(cmd["vx"]) > 0:
    #     tripod.update(dt * SPEED, robot.legs, 50 * cmd["vx"])

    if cmd["rt"] < 0.5:
        # if abs(cmd["lx"]) > 0 or abs(cmd["ly"]) > 0 or abs(cmd["rx"]) > 0:
        #     robot.tripod.update(dt * SPEED, robot.legs, 35 * cmd["rx"], 50 * cmd["ly"], cmd["lx"] * 25)
        # else:
        #     robot.tripod.reset()
        #     robot.home()

        brain.set_velocities(35 * cmd["rx"], 50 * cmd["ly"], cmd["lx"] * 25)
        brain.set_offset((0,0,0), 0,0,0)
        #brain.set_offset((0,0,0), 0,0,0)
        if abs(cmd["hy"]) == 1:
            Height += 3 * dt * cmd["hy"]
            robot.set_height(Height)
        if abs(cmd["hx"]) == 1:
            SPEED += 3 * dt * cmd["hx"]
    else:
        #robot.move_body(Vec3(cmd["lx"], cmd["ly"], Height) * Strength, 0, cmd["rx"] * Angle, cmd["ry"] * Angle)
        brain.set_offset(Vec3(cmd["lx"], cmd["ly"], 0) * Strength, 0, cmd["rx"] * Angle, cmd["ry"] * Angle)
        if abs(cmd["hy"]) == 1:
            Strength += 3 * dt * cmd["hy"]
        if abs(cmd["hx"]) == 1:
            Angle += 3 * dt * cmd["hx"]


    # if counter % 100:
    #     print(cmd)
    #     print(SPEED, Strength, Angle)
    counter += 1
    brain.update(dt * SPEED)
    # if current_command == "w":
    #     tripod.update(dt * SPEED, robot.legs, 50)
    #     time.sleep(DT)
    # elif current_command == "s":
    #     tripod.update(dt * SPEED, robot.legs, -50)
    # else:
    #     robot.home()
    time.sleep(1 / 50)