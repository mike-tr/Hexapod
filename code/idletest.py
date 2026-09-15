# from Initialization.servo import ServoController
# from Initialization.leg import HexLeg
from Initialization.pca9685 import PCA9685
from Initialization.adc import ADC
from Initialization.hexapodConfig import HexapodConfig
from Initialization.tripodgait import TripodGait
import time

# print("Testing remote pi")

robot = HexapodConfig()

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
        robot.legR[0].set_angles(0, 80, last)
        # robot.legR[1].set_angles(0, 80, last)
        # robot.legR[2].set_angles(0, 80, last)
        time.sleep(1)
        
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
