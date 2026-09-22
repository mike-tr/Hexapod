
from __future__ import annotations
import time
import sys
import os
import math

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from typing import TYPE_CHECKING
from vector import Vec3
if TYPE_CHECKING:
    from leg import HexLeg

class TripodGait:
    # PHASE = (0, 0.5, 0, 0.5, 0, 0.5)
    # DUTY = 0.5
    PHASE = (0, 1/3, 2/3, 1/2, 5/6, 1/6)
    DUTY = 2/3
    DUAL_GAIT = 0
    TRIPLE_GAIT = 1

    def __init__(self, norm_factor, max_reach, period=1.0, lift=25.0):
        self.period, self.lift = period, lift
        self.norm_factor = norm_factor
        self.max_reach = max_reach
        self._t = 0.0
        self.swing_bulge = 25 * norm_factor
        self.load_gait(self.DUAL_GAIT)

    def load_gait(self, gate):
        if gate == self.DUAL_GAIT:
            self.DUTY = 2/3
            self.PHASE = (0, 1/3, 2/3, 1/2, 5/6, 1/6)
        else:
            self.PHASE = (0, 0.5, 0, 0.5, 0, 0.5)
            self.DUTY = 0.5

    def reset(self):
        self._t = 0.0

    def foot_delta(self, phase, stroke, leg : HexLeg):
        #print("phase :", phase)
        sx, sy = stroke
        hx, hy, hz = leg._aligned_home
        if phase < self.DUTY:
            # Foot on the ground
            u = phase / self.DUTY
            k = (u - 0.5) * self.norm_factor
            return Vec3(hx + sx * k, hy - sy * k, hz)
        u = (phase - self.DUTY) / (1 - self.DUTY)
        k = (u - 0.5) * self.norm_factor
        bulge = leg.orientation * self.swing_bulge * math.sin(math.pi * u)
        return Vec3(hx + sx * k + bulge, hy + sy * k, hz + self.lift * math.sin(math.pi * u) * self.norm_factor)

    def stroke(self, leg : HexLeg, vx, vy, omega):
        T = self.period * self.DUTY      # stance duration
        #hx, hy = leg.home_body_xy         # neutral foot pos, body frame
        return (-(vx - omega * leg.home_body_pos.y * 0.01)) * T, (-(vy + omega * leg.home_body_pos.x * 0.01)) * T

    

    def update(self, dt, legs : list[HexLeg], vx, vy, omega):
        self._t = (self._t + dt / self.period) % 1.0
        #print("time : ", self._t)

        commands = []
        max_length = 0
        for leg, ph in zip(legs, self.PHASE):
            d = self.foot_delta((self._t + ph) % 1.0, self.stroke(leg, vx, vy, omega), leg)
            length = d.lengthSquared()
            if length > max_length:
                max_length = length
            commands.append(d)

        factor = 1
        if max_length > self.max_reach**2:
            factor = self.max_reach / math.sqrt(max_length)
        for leg, command in zip(legs, commands):
            #print("what is that", d)
            if factor > 1:
                command *= factor
            leg.move_leg_aligned(command)
            #leg.move_leg_aligned()
            