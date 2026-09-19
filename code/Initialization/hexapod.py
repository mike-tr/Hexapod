import time
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pca9685 import PCA9685

from leg import HexLeg
from servo import ServoController
from iksystem import IKSystem3
from config_init import Config
from vector import Vec3
from tripodgait import TripodGait

class Hexapod:
    HOME_LOCAL : Vec3
    HOME_RELAXED : Vec3
    
    """Servo channel mapping and physical parameters for this hexapod."""
    def __init__(self):
        self.controller = ServoController()
        hexdata = Config()
        hexdata.load()
        self.iksys = IKSystem3(hexdata.data["COXA_LENGTH"], hexdata.data["FEMUR_LENGTH"], hexdata.data["TIBIA_LENGTH"])
        # self.HOME_RELAXED = hexdata.data["HOME_RELAXED"]
        # self.HOME_LOCAL = hexdata.data["HOME_POS"]

        self.norm_to_mm_factor = self.iksys.max_reach / hexdata.data["POSITION_SCALE"]
        self.HOME_RELAXED = Vec3(*hexdata.data["HOME_RELAXED_NORM"]) * self.norm_to_mm_factor
        self.HOME_LOCAL = Vec3(*hexdata.data["HOME_POS_NORM"]) * self.norm_to_mm_factor
        print(self.HOME_RELAXED, self.HOME_LOCAL)


        self.legR : list[HexLeg] = []
        self.legL : list[HexLeg] = []

        #print(hexdata.data)
        for leg in hexdata.LEGS:
            if leg[0] == 'R':
                self.legR.append(HexLeg(leg, self, hexdata.data["LEGS"][leg], hexdata.data["TIBIA_CURVE"]))
            else:
                self.legL.append(HexLeg(leg, self,  hexdata.data["LEGS"][leg], hexdata.data["TIBIA_CURVE"]))
        self.legs = self.legL + self.legR

        self.tripod = TripodGait(self.norm_to_mm_factor, 2, 40)
        self.tripod.load_gait(TripodGait.TRIPLE_GAIT)

    # @property
    # def legs(self) -> Servo:
    #     return

    def home(self):
        for leg in self.legs:
            leg.home()

    def relaxed_home(self):
        for leg in self.legs:
            print(self.HOME_RELAXED)
            leg.move_leg(self.HOME_RELAXED)

    def extended(self):
        for leg in self.legs:
            leg.set_angles(0, 0, 90)

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