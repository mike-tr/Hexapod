from Initialization.servo import Servo
from Initialization.pca9685 import PCA9685
from Initialization.adc import ADC
import time

# print("Testing remote pi")

servo = Servo()


legs = [
    [15, 14, 13],
    [12, 11, 10],
    [9, 8, 31],
    [16, 17, 18],
    [19,20,21],
    [22,23,27]
]


pwm = PCA9685(0x41, debug=True)

id=20
# Try to relax channel 0 directly
servo.set_angle(id, 140)
time.sleep(3)
servo.relax(id)
print("Relaxed. Try moving the leg by hand now.")
time.sleep(30)


# while True:
#     try:

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

