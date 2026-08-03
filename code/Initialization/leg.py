import time
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from servo import Servo, ServoController

class HexLeg:
    COXA = 0
    FEMUR = 1
    TIBIA = 2
    NUM_JOINTS = 3

    def __init__(self, controller : ServoController, coxa_servo_id, femur_servo_id, tibia_servo_id):
        #self.controller : ServoController = controller
        self.servos: list[Servo] = [
            Servo(controller, coxa_servo_id),
            Servo(controller, femur_servo_id),
            Servo(controller, tibia_servo_id),
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
    
    def moveLeg(self, right: bool, id: int, x, y, z):
        pass

    def set_angles(self, coxa_angle, femur_angle, tibia_angle):
        self.coxa.set_angle(coxa_angle)
        self.femur.set_angle(femur_angle)
        self.tibia.set_angle(tibia_angle)

    def set_angles_from_list(self, angles: list[float]) -> None:
        """Set all three joint angles from a list [coxa, femur, tibia]."""
        if len(angles) != self.NUM_JOINTS:
            raise ValueError(f"Expected {self.NUM_JOINTS} angles, got {len(angles)}")
        for servo, angle in zip(self.servos, angles):
            servo.set_angle(angle)

    def relax(self):
        """De-energize all three servos."""
        for servo in self.servos:
            servo.relax()