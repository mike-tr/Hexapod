import socket, json, time, pygame

ROBOT = ("192.168.10.21", 9000)   # your Pi's IP

pygame.init()
pygame.joystick.init()
js = pygame.joystick.Joystick(0)
js.init()
print("using:", js.get_name())

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def deadzone(v, t=0.12):
    return 0.0 if abs(v) < t else (v - t * (1 if v > 0 else -1)) / (1 - t)

while True:
    pygame.event.pump()
    hx, hy = js.get_hat(0)
    for i in range(js.get_numaxes()):
        print(i, round(js.get_axis(i), 2))
    msg = {
        "lx":    -deadzone(js.get_axis(0)),
        "ly":     deadzone(js.get_axis(1)),
        "rx":  deadzone(js.get_axis(2)),
        "ry":  deadzone(js.get_axis(3)),
        "hx": hx,
        "hy": hy,
        "rt":  deadzone(js.get_axis(5))
    }
    print(msg)
    sock.sendto(json.dumps(msg).encode(), ROBOT)
    time.sleep(1 / 50)