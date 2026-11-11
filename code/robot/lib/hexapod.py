import time
import sys
import os

from robot.lib.drivers.pca9685 import PCA9685

from robot.lib.leg import HexLeg
from robot.lib.drivers.servo import ServoController
from robot.lib.iksystem import IKSystem3
from common.config_init import Config
from common.vector import Vec3
from robot.lib.gait import TripodGait

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
        print("relaxed", self.HOME_RELAXED, "locla", self.HOME_LOCAL)


        self.legR : list[HexLeg] = []
        self.legL : list[HexLeg] = []

        #print(hexdata.data)
        for leg in hexdata.LEGS:
            if leg[0] == 'R':
                self.legR.append(HexLeg(leg, self, hexdata.data["LEGS"][leg], hexdata.data["TIBIA_CURVE"]))
            else:
                self.legL.append(HexLeg(leg, self,  hexdata.data["LEGS"][leg], hexdata.data["TIBIA_CURVE"]))
        self.legs = self.legL + self.legR

        self.max_reach = hexdata.data["COXA_LENGTH"] + hexdata.data["FEMUR_LENGTH"] + hexdata.data["TIBIA_LENGTH"]
        self.height_offset = Vec3(0, 0, 0)
        # self._walking = False

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
        d = 1/60
        t = 0
        while(t < 1):
            p = self.HOME_RELAXED * t + self.HOME_LOCAL * (1 - t)
            for leg in self.legs:
                leg.move_leg(p)

            t += d
            time.sleep(d)
        

        for leg in self.legs:
            leg.relax()

        # if self._walking or self.tripod:
        #     self.tripod.update(dt, self.legs, self.vx, self.omega)

    def set_height(self, height):
        self.height_offset = Vec3(0, 0, height)


    def move_body(self, pose : Vec3, yaw_deg, roll_deg, pitch_deg):
        """
        Move the hexapod body from its natural standing position to pos, and then apply body rotations.
        Note, that the since y is forward, and x is sideways roll and pitch are reversed.
        """
        for leg in self.legs:
            p : Vec3 = leg.home_body_pos - pose - self.height_offset
            #print(p)
            leg.move_leg_body(p.rotate_inv(yaw_deg, roll_deg, -pitch_deg))

    # def moveLegAngle(self, right: bool, id: int, coxa_angle, femur_angle, tibia_angle):
    #     if right:
    #         pass