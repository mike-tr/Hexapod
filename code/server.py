import socket, json, time
from Initialization.servo import Servo
from Initialization.pca9685 import PCA9685
from Initialization.adc import ADC
from Initialization.hexapod import Hexapod
from Initialization.tripodgait import TripodGait
from Initialization.vector import Vec3

PORT = 9000
WATCHDOG = 0.5  # seconds without a packet -> stop

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))
sock.setblocking(False)

cmd = {"lx": 0.0, "ly": 0.0, "rx": 0.0, "ry" : 0.0, "hx": 0.0, "hy": 0.0, "rt": -1.0}
last_rx = time.time()

robot = Hexapod()


prev = time.monotonic()
counter = 0
DT = 0.02
SPEED = 1.1
Strength = 5
Angle = 5
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
        if abs(cmd["lx"]) > 0 or abs(cmd["ly"]) > 0 or abs(cmd["rx"]) > 0:
            robot.tripod.update(dt * SPEED, robot.legs, 35 * cmd["rx"], 50 * cmd["ly"], cmd["lx"] * 25)
        else:
            robot.tripod.reset()
            robot.home()

        if cmd["hy"] == 1 and counter % 20:
            SPEED += 0.01
        if cmd["hy"] == -1 and counter % 20:
            SPEED -= 0.01
    else:
        robot.move_body(Vec3(cmd["lx"], cmd["ly"], 0) * Strength, 0, cmd["ry"] * Angle, cmd["rx"] * Angle)
        if abs(cmd["hy"]) == 1:
            Strength += 3 * dt * cmd["hy"]
        if abs(cmd["hx"]) == 1:
            Angle += 3 * dt * cmd["hx"]


    if counter % 100:
        print(cmd)
        print(SPEED, Strength, Angle)
    counter += 1
    # if current_command == "w":
    #     tripod.update(dt * SPEED, robot.legs, 50)
    #     time.sleep(DT)
    # elif current_command == "s":
    #     tripod.update(dt * SPEED, robot.legs, -50)
    # else:
    #     robot.home()
    time.sleep(1 / 50)