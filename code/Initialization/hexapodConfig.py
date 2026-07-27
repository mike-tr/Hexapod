from leg import HexLeg
from servo import Servo, ServoController


class HexapodConfig:
    """Servo channel mapping and physical parameters for this hexapod."""
    def __init__(self):
        self.controller = ServoController()
        self.legR : list[HexLeg] = [HexLeg(self.controller,18,17,16), HexLeg(self.controller,21,20,19), HexLeg(self.controller,27,23,22)]
        self.legL : list[HexLeg] = [HexLeg(self.controller,13,14,15), HexLeg(self.controller,10,11,12), HexLeg(self.controller,31,8,9)]


    def moveLegAngle(self, right: bool, id: int, coxa_angle, femur_angle, tibia_angle):
        if right:
            self.legR[id].se