import time
import sys
import os
import math

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from servo import Servo, ServoController
from iksystem import IKSystem3
from hexapodConfig import HexapodConfig

class HexLeg:
    COXA = 0
    FEMUR = 1
    TIBIA = 2
    NUM_JOINTS = 3

    def __init__(self, config : HexapodConfig, coxa_servo_id, femur_servo_id, tibia_servo_id, rotation, mount_position):
        #self.controller : ServoController = controller
        self._ik : IKSystem3 = config.iksys
        self._rsin = math.sin(-math.radians(rotation))
        self._rcos = math.cos(-math.radians(rotation))
        self._mount_x = mount_position[0]
        self._mount_y = mount_position[1]
        self._mount_z = mount_position[2]
        self.servos: list[Servo] = [
            Servo(config.controller, coxa_servo_id),
            Servo(config.controller, femur_servo_id),
            Servo(config.controller, tibia_servo_id),
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

    def move_leg_body(self, x, y, z):
        """Absolute point in body frame (origin = body center)."""
        self.move_leg(x - self._mount_x, y - self._mount_y, z - self.mount_z)
    
    def move_leg(self, x, y, z):
        self.move_leg_local(self._rcos * x - self._rsin * y, self._rsin * x + self._rcos * y, z)

    def move_leg_local(self, x, y, z):
        self.set_angles_from_list(self.ik.angles_from_position_normalized(x,y,z))

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