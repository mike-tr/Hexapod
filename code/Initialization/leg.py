from __future__ import annotations
import time
import sys
import os
import math

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from servo import Servo, ServoConfig
from iksystem import IKSystem3


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from hexapodConfig import HexapodConfig

class HexLeg:
    COXA = 0
    FEMUR = 1
    TIBIA = 2
    NUM_JOINTS = 3

    def __init__(self, id, config : HexapodConfig,  coxa : ServoConfig, femur : ServoConfig, tibia : ServoConfig, rotation, mount_position, home_position):
        #self.controller : ServoController = controller
        self.id = id
        self._ik : IKSystem3 = config.iksys
        self._rsin = math.sin(math.radians(rotation))
        self._rcos = math.cos(math.radians(rotation))
        self._local_home = home_position
        self._aligned_home = self.aligned_pos(home_position[0], home_position[1], home_position[2])

        self.orientation = 1
        if(math.fabs(rotation) > 90):
            self.orientation = -1
    

        self._mount_x = mount_position[0]
        self._mount_y = mount_position[1]
        self._mount_z = mount_position[2]

        print(id, rotation, mount_position, math.degrees(math.atan2(self._mount_y, self._mount_x)), self.orientation)

        self._local_x = 0
        self._local_y = 0
        self._local_z = 0
        self.servos: list[Servo] = [
            Servo(config.controller, coxa),
            Servo(config.controller, femur),
            Servo(config.controller, tibia),
        ]

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

    def body_pos(self, x, y, z):
        """transforms position in local space to position in body"""
        nx = self._rcos * x - self._rsin * y + self._mount_x
        ny = self._rsin * x + self._rcos * y + self._mount_y
        return (nx, ny, z + self._mount_z)

    def aligned_pos(self, x, y, z):
        """transforms position in local space to aligned position"""
        nx = self._rcos * x - self._rsin * y
        ny = self._rsin * x + self._rcos * y
        return (nx, ny, z)

    def move_leg_body(self, x, y, z):
        """Absolute point in body frame (origin = body center)."""
        self.move_leg(x - self._mount_x, y - self._mount_y, z - self.mount_z)
    
    def move_leg_aligned(self, x, y, z):
        """Body-aligned axes, origin at this leg's coxa axis.

        Use for translation deltas — mount offset cancels, so all six
        legs take the same vector. For rotation, use move_leg_body().
        """
        self.move_leg_local(self._rcos * x + self._rsin * y, - self._rsin * x + self._rcos * y, z)

    def move_leg_local(self, x, y, z):
        """Absolute point in leg frame."""
        self._local_y = y
        self._local_z = z
        self._local_x = x
        print("pos")
        print(x,y,z)
        self.set_angles_from_list(self._ik.angles_from_position_normalized(x,y,z))

    def home(self):
        self.move_leg_local(self._local_home[0], self._local_home[1], self._local_home[2])

    def set_angles(self, coxa_angle, femur_angle, tibia_angle):
        self.coxa.set_angle(coxa_angle)
        self.femur.set_angle(femur_angle)
        self.tibia.set_angle(tibia_angle)

    def set_angles_from_list(self, angles: list[float]) -> None:
        """Set all three joint angles from a list [coxa, femur, tibia]."""
        if len(angles) != self.NUM_JOINTS:
            raise ValueError(f"Expected {self.NUM_JOINTS} angles, got {len(angles)}")
        print(angles)
        for servo, angle in zip(self.servos, angles):
            servo.set_angle(angle)

    def relax(self):
        """De-energize all three servos."""
        for servo in self.servos:
            servo.relax()