from leg import HexLeg

class HexapodConfig:
    """Servo channel mapping and physical parameters for this hexapod."""
    def __init__(self):
        self.legR = [HexLeg(18,17,16), HexLeg(21,20,19), HexLeg(27,23,22)]
        self.legL = [HexLeg(13,14,15), HexLeg(10,11,12), HexLeg(31,8,9)]