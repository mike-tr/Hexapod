# from Initialization.servo import ServoController
# from Initialization.leg import HexLeg
from Initialization.pca9685 import PCA9685
from Initialization.adc import ADC
from Initialization.hexapod import Hexapod
from Initialization.tripodgait import TripodGait
from Initialization.vector import Vec3
import time

# print("Testing remote pi")

robot = Hexapod()

tripod = TripodGait(2, 50)
tripod.load_gait(TripodGait.TRIPLE_GAIT)

foot = 125
center = 70
rotation = 90

id = 0

# robot.legR[0].set_angles(90, 90, 135)
# time.sleep(6)
robot.relax()
time.sleep(1)
# robot.home()
# time.sleep(3)
last = 90
try:
    while True:
        # robot.legL[0].set_angles(0, 0, last)
        # robot.legL[1].set_angles(0, 0, last)
        # robot.legL[2].set_angles(0, 0, last)
        #robot.legR[0].set_angles(0, 30, last)
        leg = robot.legL[2]
        leg.set_angles(0, 80, last)
        #leg.move_leg_body(leg.home_body_pos - Vec3(40,20,-90))
        print(leg.name, leg._current_pos)
        # robot.legR[1].set_angles(0, 80, last)
        # robot.legR[2].set_angles(0, 80, last)
        time.sleep(4)
        leg.set_angles(40, 70, last)
        time.sleep(2)
        # #leg.move_leg_body(leg.home_body_pos - Vec3(40,100,-90))
        # print(leg.name, leg._current_pos)
        # time.sleep(1)
        # robot.legR[0].set_angles(0, 90, last)
        # robot.legR[1].set_angles(0, 30, last)
        # robot.legR[2].set_angles(0, 90, last)
        # robot.legL[0].set_angles(0, 30, last)
        # robot.legL[1].set_angles(0, 90, last)
        # robot.legL[2].set_angles(0, 30, last)
        # # tripod.update(0.01, robot.legs, 50)
        # time.sleep(3)
        # robot.legL[0].set_angles(0, 30, last)
        # robot.legL[1].set_angles(0, 30, last)
        # robot.legL[2].set_angles(0, 30, last)
        # robot.legR[0].set_angles(0, 30, last)
        # robot.legR[1].set_angles(0, 30, last)
        # robot.legR[2].set_angles(0, 30, last)
        # time.sleep(1)
        # robot.legL[0].set_angles(0, 90, last)
        # robot.legL[1].set_angles(0, 30, last)
        # robot.legL[2].set_angles(0, 90, last)
        # robot.legR[0].set_angles(0, 30, last)
        # robot.legR[1].set_angles(0, 90, last)
        # robot.legR[2].set_angles(0, 30, last)
        # time.sleep(3)

except KeyboardInterrupt:
    print("\nProgram stopped by user. Relaxing robot...")
    
finally:
    # This block always runs, ensuring the robot relaxes safely
    #robot.legR[0].home()
    time.sleep(1) # Optional brief pause before relaxing
    robot.relax()
    print("Robot relaxed successfully.")
