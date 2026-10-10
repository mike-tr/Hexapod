from Initialization.vector import Vec3
from Initialization.hexapod import Hexapod
import time

p = Vec3(0, 1, 0)
print(p)
print(p.rotate_inv(0,0,0))

robot = Hexapod()

print("R0", robot.legR[0].name)

for leg in robot.legs:
    print(leg.name, leg._mount_pos, leg._aligned_home, leg.home_body_pos)

print(" -------------- HOME ------------------")
robot.home()

for leg in robot.legs:
    #print(leg.name,  leg._current_pos)
    print(leg.name, leg.local_to_body(leg._current_pos))

time.sleep(2)

print(" -------------- HOME + (0, 20 , 0) ------------------")
robot.move_body(Vec3(0, 40, 0), 0, 0, 0)

for leg in robot.legs:
    #print(leg.name, leg._current_pos)
    print(leg.name, leg.local_to_body(leg._current_pos))

time.sleep(2)
robot.relax()