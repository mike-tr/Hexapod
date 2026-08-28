import time
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pca9685 import PCA9685

from leg import HexLeg
from servo import ServoController
from iksystem import IKSystem3
from config_init import Config

class HexapodConfig:
    HOME_LOCAL : tuple[float, float, float]
    HOME_RELAXED : tuple[float, float, float]
    
    """Servo channel mapping and physical parameters for this hexapod."""
    def __init__(self):
        self.controller = ServoController()
        hexdata = Config()
        hexdata.load()
        self.HOME_RELAXED = hexdata.data["HOME_RELAXED"]
        self.HOME_LOCAL = hexdata.data["HOME_POS"]
        self.iksys = IKSystem3(hexdata.data["COXA_LENGTH"], hexdata.data["FEMUR_LENGTH"], hexdata.data["TIBIA_LENGTH"])

        self.legR : list[HexLeg] = []
        self.legL : list[HexLeg] = []

        #print(hexdata.data)
        for leg in hexdata.LEGS:
            if leg[0] == 'R':
                self.legR.append(HexLeg(leg, self, hexdata.data["LEGS"][leg]))
            else:
                self.legL.append(HexLeg(leg, self,  hexdata.data["LEGS"][leg]))
        self.legs = self.legL + self.legR

    # @property
    # def legs(self) -> Servo:
    #     return 

    def home(self):
        for leg in self.legs:
            leg.home()

    def relaxed_home(self):
        for leg in self.legs:
            leg.move_leg_local(self.HOME_RELAXED)

    def relax(self):
        for leg in self.legs:
            leg.relax()
        # for leg in self.legR:
        #     leg.relax()
        # for leg in self.legL:
        #     leg.relax()

    # def moveLegAngle(self, right: bool, id: int, coxa_angle, femur_angle, tibia_angle):
    #     if right:
    #         pass