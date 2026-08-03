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

class HexapodConfig:
    """Servo channel mapping and physical parameters for this hexapod."""
    def __init__(self):
        self.controller = ServoController()
        self.iksys = IKSystem3(COXA_LENGTH, ZERO_ANGLE1, FEMUR_LENGTH, ZERO_ANGLE2, TIBIA_LENGTH, ZERO_ANGLE3)
        self.legR : list[HexLeg] = [HexLeg(self.controller,18,17,16), HexLeg(self.controller,21,20,19), HexLeg(self.controller,27,23,22)]
        self.legL : list[HexLeg] = [HexLeg(self.controller,13,14,15), HexLeg(self.controller,10,11,12), HexLeg(self.controller,31,8,9)]

    def relax(self):
        for leg in self.legR:
            leg.relax()
        for leg in self.legL:
            leg.relax()

    # def moveLegAngle(self, right: bool, id: int, coxa_angle, femur_angle, tibia_angle):
    #     if right:
    #         pass