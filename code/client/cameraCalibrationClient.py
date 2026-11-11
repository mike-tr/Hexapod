import pygame, json, socket, cv2
from cameraClient import FrameReceiver

pygame.init()
pygame.joystick.init()
js = pygame.joystick.Joystick(0)

W, H = 1280, 720
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("hexapod")
surf = pygame.Surface((W, H))
clock = pygame.time.Clock()


reciever = FrameReceiver()

ROBOT = ("192.168.10.21", 9000)   # your Pi's IP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def deadzone(v, t=0.12):
    return 0.0 if abs(v) < t else (v - t * (1 if v > 0 else -1)) / (1 - t)

running = True
reciever.start()
while running:
    shoot = False
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                shoot = True
            elif e.key == pygame.K_ESCAPE:
                running = False

    hx, hy = js.get_hat(0)
    msg = {
        "lx": -deadzone(-js.get_axis(0)),
        "ly":  deadzone(-js.get_axis(1)),
        "rx":  deadzone(js.get_axis(2)),
        "ry":  deadzone(-js.get_axis(3)),
        "hx": hx,
        "hy": hy,
        "rt":  deadzone(js.get_axis(5)),
        "shoot": shoot,
        "stop": False
    }
    sock.sendto(json.dumps(msg).encode(), ROBOT)
    print(msg)

    frame = reciever.frame
    if frame is not None:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pygame.surfarray.blit_array(surf, rgb.swapaxes(0, 1))
        screen.blit(surf, (0, 0))

    pygame.display.flip()
    clock.tick(50)

pygame.quit()