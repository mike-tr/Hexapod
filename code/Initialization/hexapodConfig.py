import time
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pca9685 import PCA9685

from leg import HexLeg
from servo import Servo, ServoController
from iksystem import IKSystem3

COXA_LENGTH = 60.3
FEMUR_LENGTH = 89.5
TIBIA_LENGTH = 121.5
ZERO_ANGLE1 = 90
ZERO_ANGLE2 = 90
ZERO_ANGLE3 = 45


MOUNT_POSX_0D = 100.1
MOUNT_POSX_0Y = 0
MOUNT_POSX_45D = 75.13
MOUNT_POSY_45D= 96.52
MOUNT_Z_OFFSET = 0.0

class HexapodConfig:
    """Servo channel mapping and physical parameters for this hexapod."""
    def __init__(self):
        self.controller = ServoController()
        self.iksys = IKSystem3(COXA_LENGTH, ZERO_ANGLE1, FEMUR_LENGTH, ZERO_ANGLE2, TIBIA_LENGTH, ZERO_ANGLE3)
        self.legR : list[HexLeg] = [HexLeg("RT", self.controller,18,17,16, -45, (MOUNT_POSX_45D, MOUNT_POSY_45D, MOUNT_Z_OFFSET)), 
                                    HexLeg("RM", self.controller,21,20,19, 0 , (MOUNT_POSX_0D, MOUNT_POSX_0Y, MOUNT_Z_OFFSET)), 
                                    HexLeg("RB", self.controller,27,23,22, 45, (MOUNT_POSX_45D, -MOUNT_POSY_45D, MOUNT_Z_OFFSET))]
        self.legL : list[HexLeg] = [HexLeg("LT", self.controller,13,14,15, -45+180, (-MOUNT_POSX_45D, MOUNT_POSY_45D, MOUNT_Z_OFFSET)), 
                                    HexLeg("LM", self.controller,10,11,12, 180, (-MOUNT_POSX_0D, MOUNT_POSX_0Y, MOUNT_Z_OFFSET)), 
                                    HexLeg("LB", self.controller,31,8,9, 180+45, (-MOUNT_POSX_45D, -MOUNT_POSY_45D, MOUNT_Z_OFFSET))]

    def relax(self):
        for leg in self.legR:
            leg.relax()
        for leg in self.legL:
            leg.relax()

    # def moveLegAngle(self, right: bool, id: int, coxa_angle, femur_angle, tibia_angle):
    #     if right:
    #         pass