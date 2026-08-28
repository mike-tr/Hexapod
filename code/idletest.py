# from Initialization.servo import ServoController
# from Initialization.leg import HexLeg
from Initialization.pca9685 import PCA9685
from Initialization.adc import ADC
from Initialization.hexapodConfig import HexapodConfig
import time

# print("Testing remote pi")

robot = HexapodConfig()

foot = 125
center = 70
rotation = 90

id = 0

# robot.legR[0].set_angles(90, 90, 135)
# time.sleep(6)
robot.relax()

last = 90
try:
    while True:
        # robot.legR[0].set_angles(0, 0, last)
        # robot.legR[1].set_angles(0, 0, last)
        # robot.legR[2].set_angles(0, 0, last)
        # robot.legL[0].set_angles(0, 0, last)
        # robot.legL[1].set_angles(0, 0, last)
        # robot.legL[2].set_angles(0, 0, last)
        #robot.home()
        robot.relaxed_home()
        time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram stopped by user. Relaxing robot...")
    
finally:
    # This block always runs, ensuring the robot relaxes safely
    #robot.legR[0].home()
    time.sleep(1) # Optional brief pause before relaxing
    robot.relax()
    print("Robot relaxed successfully.")
