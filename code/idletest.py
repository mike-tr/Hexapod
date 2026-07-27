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

robot.legR[0].set_angles(90, 90, 90)
time.sleep(3)
robot.legR[0].set_angles(90, 90, 170)
time.sleep(3)
robot.legR[0].set_angles(90, 90, 15)
time.sleep(3)
robot.legR[0].set_angles(90, 170, 90)
time.sleep(3)
robot.legR[0].set_angles(90, 15, 90)
time.sleep(3)
robot.legR[0].set_angles(170, 90, 90)
time.sleep(3)
robot.legR[0].set_angles(15, 90, 90)

# def anim(foot, center, rotation):
#     for leg in legs:
#         for i in range(3):
#             if i == 0:
#                 servo.set_angle(leg[i], foot)
#             elif i == 1:
#                 servo.set_angle(leg[i], center)
#             else:
#                 servo.set_angle(leg[i], rotation)



# while True:
#     try:
#         anim(foot, center, rotation)
#         time.sleep(3)
#         servo.set_angle(23, 170)
#         servo.set_angle(14, 170)
#         time.sleep(3)
#         anim(foot, center, rotation)
#         time.sleep(3)
#         servo.set_angle(20, 170)
#         servo.set_angle(14, 170)
#         servo.set_angle(8, 170)
#         time.sleep(3)
#         anim(foot, center, rotation)
#         time.sleep(3)
#         servo.set_angle(17, 170)
#         servo.set_angle(8, 170)
#         time.sleep(3)
#         anim(foot, center, rotation)
#         time.sleep(3)
#         servo.set_angle(11, 170)
#         servo.set_angle(17, 170)
#         servo.set_angle(23, 170)
#         time.sleep(3)
#     except KeyboardInterrupt:
#         print("\nEnd of program")
#         for leg in legs:
#             for i in range(3):
#                 servo.relax(leg[i])
#         break


# for i in [13,14,15]:
#     servo.set_angle(i, 10)
#     time.sleep(3)
#     servo.set_angle(i, 170)
#     time.sleep(3)
#     servo.set_angle(i, 90)
# servo.relax()

