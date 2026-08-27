# from Initialization.servo import ServoController
# from Initialization.leg import HexLeg
from Initialization.pca9685 import PCA9685
from Initialization.adc import ADC
from Initialization.hexapodConfig import HexapodConfig
import time

# print("Testing remote pi")

robot = HexapodConfig()
robot.relax()

