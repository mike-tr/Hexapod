from __future__ import annotations
import time
import sys
import os
import math

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from servo import Servo
from iksystem import IKSystem3
from vector import Vec3
from config_init import Config


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from hexapod import Hexapod


class HexLeg:
    COXA = 0
    FEMUR = 1
    TIBIA = 2
    NUM_JOINTS = 3

    def __init__(self, name, brain : Hexapod, jdata, tibia_curve):
        #self.controller : ServoController = controller
        #print(jdata)
        self._current_pos : Vec3
        self.servos: list[Servo]
        self._rsin : float
        self._rcos : float
        self._local_home : Vec3
        self._aligned_home : Vec3
        self.orientation : int
        self._mount_pos : Vec3
        self.home_body_xy : tuple[float, float]

        self.brain = brain
        self.name = name
        self._ik : IKSystem3 = brain.iksys
        self.reload(jdata, tibia_curve)

        v = Vec3(40, 0, -30)
        r = self.body_to_local(self.local_to_body(v))
        assert all(abs(a - b) < 1e-9 for a, b in zip(r, v)), f"{self.name}: frame round-trip failed"
        print(self.name, self.local_to_body(Vec3(40, 0, -30)))

    def reload(self, jdata, tibia_curve):
        self._current_pos = Vec3(0, 0, 0)

        self._rsin = math.sin(math.radians(jdata["mount_angle"]))
        self._rcos = math.cos(math.radians(jdata["mount_angle"]))

        self._local_home = self.brain.HOME_LOCAL
        self._aligned_home = self.local_to_aligned(self.brain.HOME_LOCAL)

        self.orientation = 1
        if(math.fabs(jdata["mount_angle"]) > 90):
            self.orientation = -1
    
        self._mount_pos = Vec3(*jdata["mount_position"])
        # self.home_body_xy = (self._aligned_home[0] + self._mount_pos[0],
        #         self._aligned_home[1] + self._mount_pos[1])


        self.servos: list[Servo] = []
        for servo in Config.JOINTS:
            if servo == "TIBIA":
                #print("before : ", jdata[servo]["rotation_offset"])
                jdata[servo]["rotation_offset"] += tibia_curve
                #print("after : ", jdata[servo]["rotation_offset"])
            self.servos.append(Servo(self.brain.controller, jdata[servo]))


    # Named property access — enables readable individual joint access
    @property
    def coxa(self) -> Servo:
        return self.servos[self.COXA]
    
    @property
    def femur(self) -> Servo:
        return self.servos[self.FEMUR]
    
    @property
    def tibia(self) -> Servo:
        return self.servos[self.TIBIA]

    @property
    def home_body_pos(self) -> Vec3:
        return self.local_to_body(self._local_home)

    def home(self):
        self.move_leg(self._local_home)

    def local_to_aligned(self, pos : Vec3):
        """transforms position in local space to position in aligned space (i.e. centred around leg, but axes aligned with body)"""
        nx = self._rcos * pos.x - self._rsin * pos.y
        ny = self._rsin * pos.x + self._rcos * pos.y
        return Vec3(nx, ny, pos.z)

    def aligned_to_local(self, pos : Vec3):
        nx = self._rcos * pos.x + self._rsin * pos.y
        ny = -self._rsin * pos.x + self._rcos * pos.y
        return Vec3(nx, ny, pos.z)

    def aligned_to_body(self, pos: Vec3):
        return pos + self._mount_pos

    def body_to_aligned(self, pos: Vec3):
        return pos - self._mount_pos

    def local_to_body(self, pos : Vec3):
        """transforms position in local space to position in body"""
        return self.aligned_to_body(self.local_to_aligned(pos))

    def body_to_local(self, pos : Vec3):
        return self.aligned_to_local(self.body_to_aligned(pos))

    def move_leg_body(self, pos : Vec3):
        """Absolute point in body frame (origin = body center)."""
        self.move_leg(self.body_to_local(pos))

    ######################### FIXED till here
    def move_leg_aligned(self, pos : Vec3):
        """Body-aligned axes, origin at this leg's coxa axis.

        Use for translation deltas — mount offset cancels, so all six
        legs take the same vector. For rotation, use move_leg_body().
        """
        self.move_leg(self.aligned_to_local(pos))

    def move_leg(self, pos : Vec3):
        """Absolute point in leg frame."""
        self._current_pos = pos
        self.set_angles_from_list(self._ik.angles_from_position(pos))

    def set_angles(self, coxa_angle, femur_angle, tibia_angle):
        #print(coxa_angle, femur_angle, tibia_angle)
        self.coxa.set_angle(coxa_angle)
        self.femur.set_angle(femur_angle)
        self.tibia.set_angle(tibia_angle)

    def set_angles_from_list(self, angles: list[float]) -> None:
        """Set all three joint angles from a list [coxa, femur, tibia]."""
        if len(angles) != self.NUM_JOINTS:
            raise ValueError(f"Expected {self.NUM_JOINTS} angles, got {len(angles)}")
        #print(self.name, angles)
        for servo, angle in zip(self.servos, angles):
            servo.set_angle(angle)

    def relax(self):
        """De-energize all three servos."""
        for servo in self.servos:
            servo.relax()