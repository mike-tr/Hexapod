from Initialization.servo import Servo
from Initialization.pca9685 import PCA9685
from Initialization.adc import ADC
from Initialization.hexapodConfig import HexapodConfig
from Initialization.tripodgait import TripodGait
import time


# def test_Adc():
#     adc = ADC()
#     try:
#         while True:
#             Power=adc.read_battery_voltage()
#             print ("The battery voltage is "+str(Power)+'\n')
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print ("\nEnd of program")

# test_Adc()


robot = HexapodConfig()
# tripod = TripodGait(2, 60, 25)
# offsets = [(35, 0, -30) , (35, 0)]
# # print(time.time())

# t = time.time()
# prev = time.time()
# while(t + 5 > time.time()):
#     dt = time.time() - prev
#     #print(time.time())
#     #tripod.reset()
#     tripod.update(dt, robot.legs, )
# robot.relax()

# robot.legR[0].set_angles(90, 90, 90)

# id = 1


#robot.legL[1].move_leg_aligned(-70, 50, -10)
y=0
#time.sleep(1)
# print("Movement")
#robot.legL[0].move_leg_aligned(-35, y, -30)
# time.sleep(3)
# # robot.legR[0].move_leg_aligned(80, y, 0)
# # time.sleep(3)
# robot.legL[1].move_leg_aligned(-35, y, -30)
# time.sleep(3)
# robot.legR[1].move_leg_aligned(80, y, 0)
# time.sleep(3)
# robot.legL[2].move_leg_aligned(-80, y, 0)
# time.sleep(3)
# robot.legR[2].move_leg_aligned(80, y, 0)

# robot.legR[1].move_leg_local(0, 40, 0)
#robot.legL[1].move_leg_local(40, 70, -40)
robot.home()

time.sleep(5)


# robot.legR[0].set_angles_from_list([90, 150, 180])
# time.sleep(3)


tripod = TripodGait(2, 50)
tripod.load_gait(TripodGait.TRIPLE_GAIT)
# print(time.time())

t = time.monotonic()
prev = time.monotonic()
DT = 0.02
while(t + 10 > time.monotonic()):
    dt = time.monotonic() - prev
    prev = time.monotonic()
    #print(dt)
    #tripod.reset()
    tripod.update(dt, robot.legs, 70)
    time.sleep(DT)

# robot.home()
# time.sleep(3)
# while(t + 5 > time.monotonic()):
#     dt = time.monotonic() - prev
#     prev = time.monotonic()
#     #print(dt)
#     #tripod.reset()
#     tripod.update(dt, robot.legs, -20)
#     time.sleep(DT)

robot.relax()

# for leg in robot.legs:
#     #print(leg.id, leg._aligned_home)
#     leg.move_leg_aligned(leg._aligned_home[0], leg._aligned_home[1], leg._aligned_home[2])

#print("TTTTTTTTTTTTTTTTTTT")
# robot.legL[id].set_angles_from_list(robot.iksys.angles_from_position_normalized(70, 0, 35))
# time.sleep(1)
# robot.legL[id].set_angles_from_list(robot.iksys.angles_from_position_normalized(80, 0, -10))
# time.sleep(1)
# robot.legL[id].set_angles_from_list(robot.iksys.angles_from_position_normalized(70, 0, -10))
# time.sleep(1)
# robot.legL[id].set_angles_from_list(robot.iksys.angles_from_position_normalized(100, 0, 0))
# time.sleep(1)
# robot.legL[id].set_angles_from_list(robot.iksys.angles_from_position_normalized(100, 50, 30))
# print()
# time.sleep(1)
# robot.legL[id].set_angles_from_list(robot.iksys.angles_from_position_normalized(0.7, 0.3, -0.35))
# time.sleep(1)
# robot.legL[id].set_angles_from_list(robot.iksys.angles_from_position_normalized(0.7, 0.0, -0.35))
# time.sleep(1)
# robot.legL[id].set_angles_from_list(robot.iksys.angles_from_position_normalized(0.5, 0.4, 0.15))
# time.sleep(1)
# robot.legL[id].set_angles_from_list(robot.iksys.angles_from_position_normalized(0.5, -0.3, -0.55))
# time.sleep(1)
# robot.legL[id].set_angles_from_list(robot.iksys.angles_from_position_normalized(0.5, 0.0, -0.25))
# time.sleep(1)
# robot.legL[id].set_angles_from_list(robot.iksys.angles_from_position_normalized(0.96, 0.0, 0.15))
