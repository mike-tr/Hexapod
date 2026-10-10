from Initialization.hexapod import Hexapod
from Initialization.tripodgait import TripodGait
from Initialization.vector import Vec3

class HexapodBrain:
    def __init__(self, robot : Hexapod):
        self.robot = robot
        self.tripod = TripodGait(self.robot.norm_to_mm_factor, self.robot.max_reach, 2, 40)
        self.tripod.load_gait(TripodGait.TRIPLE_GAIT)

        self.vx = self.vy = self.omega = 0.0
        self.body_offset = Vec3(0,0,0)
        self.yaw = self.pitch = self.roll = 0.0


    def update(self, dt):
        if self.vx or self.vy or self.omega:
            self.tripod.update(dt, self.robot.legs, self.vx, self.vy, -self.omega)
        else:
            self.tripod.reset()
            self.robot.move_body(self.body_offset, self.yaw, self.roll, self.pitch)

    def set_velocities(self, vx, vy, omega):
        self.vx = vx
        self.vy = vy
        self.omega = omega

    def set_offset(self, pos: Vec3, yaw, roll, pitch):
        self.body_offset = pos
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll