from Initialization.servo import Servo
from Initialization.pca9685 import PCA9685
from Initialization.adc import ADC
from Initialization.hexapodConfig import HexapodConfig
import time

# print("Testing remote pi")

# servo = Servo()

# # Main program logic follows:
# if __name__ == '__main__':
#     print("Now servos will rotate to certain angles.")
#     print("Please keep the program running when installing the servos.")
#     print("After that, you can press ctrl-C to end the program.")
#     servo = Servo()
#     while True:
#         try:
#             for i in range(32):
#                 if i in [10, 13, 31]:
#                     servo.set_angle(i, 10)
#                 elif i in [18, 21, 27]:
#                     servo.set_angle(i, 170)
#                 else:
#                     servo.set_angle(i, 90)
#             time.sleep(3)
#         except KeyboardInterrupt:
#             print("\nEnd of program")
#             servo.relax()
#             break

# def test_Adc():
#     adc = ADC()
#     try:
#         while True:
#             Power=adc.read_battery_voltage()
#             print ("The battery voltage is "+str(Power)+'\n')
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print ("\nEnd of program")

# for i in range(10):
#     servo.set_angle(15,180)
#     print(180)
#     time.sleep(5)
#     servo.set_angle(15,0)
#     print(0)
#     time.sleep(5)
# servo.set_angle(15,135)
# time.sleep(2)
# servo.set_angle(15,45)
# time.sleep(2)
# # servo.set_angle(15,0)
# # time.sleep(3)
# # servo.set_angle(15,180)
# # time.sleep(3)
# servo.relax()

# test_Adc()

# id = 18
# servo.set_angle(id, 170)
# time.sleep(3)
# servo.set_angle(id, 10)
# time.sleep(3)
# servo.set_angle(id, 90)
# time.sleep(3)
# # servo.set_angle(15, 10)
# # time.sleep(3)
# # servo.set_angle(15, 90)
# # time.sleep(3)
# servo.relax()


# target = 160
# while True:
#     try:
#         servo.set_angle(id, target)
#         # servo.set_angle(17, target)
#         # servo.set_angle(16, target)

#         # servo.set_angle(15, target)
#         # servo.set_angle(14, target)
#         # servo.set_angle(13, target)
#         time.sleep(3)
#     except KeyboardInterrupt:
#         print("\nEnd of program")
#         servo.relax(id)
#         break

# test_Adc()

robot = HexapodConfig()

# robot.legR[0].set_angles(90, 90, 90)

id = 1


robot.legL[id].set_angles_from_list(robot.iksys.angles_from_position_normalized(0.95, 0.3, 0))
time.sleep(1)
robot.legL[id].set_angles_from_list(robot.iksys.angles_from_position_normalized(0.7, 0.3, -0.35))
time.sleep(1)
robot.legL[id].set_angles_from_list(robot.iksys.angles_from_position_normalized(0.7, 0.0, -0.35))
time.sleep(1)
robot.legL[id].set_angles_from_list(robot.iksys.angles_from_position_normalized(0.5, 0.4, 0.15))
time.sleep(1)
robot.legL[id].set_angles_from_list(robot.iksys.angles_from_position_normalized(0.5, -0.3, -0.55))
time.sleep(1)
robot.legL[id].set_angles_from_list(robot.iksys.angles_from_position_normalized(0.5, 0.0, -0.25))
