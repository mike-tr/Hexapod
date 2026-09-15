
from __future__ import annotations
import time
import sys
import os
import math

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from leg import HexLeg

class TripodGait:
    # PHASE = (0, 0.5, 0, 0.5, 0, 0.5)
    # DUTY = 0.5
    PHASE = (0, 1/3, 2/3, 1/2, 5/6, 1/6)
    DUTY = 2/3
    DUAL_GAIT = 0
    TRIPLE_GAIT = 1

    def __init__(self, period=1.0, lift=25.0):
        self.period, self.lift = period, lift
        self._t = 0.0
        self.swing_bulge = 35
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
            k = u - 0.5
            return (hx + sx * k, hy + sy * (0.5 - u), hz)
        u = (phase - self.DUTY) / (1 - self.DUTY)
        k = u - 0.5
        bulge = leg.orientation * self.swing_buldge * math.sin(math.pi * u)
        return (hx + sx * k + bulge, hy + sy * k, hz + self.lift * math.sin(math.pi * u))

    def stroke(self, leg, vx, vy, omega):
        T = self.period * self.gait.DUTY      # stance duration
        hx, hy = leg.home_body_xy         # neutral foot pos, body frame
        return (-(vx - omega * hy)) * T, (-(vy + omega * hx)) * T

    def update(self, dt, legs : list[HexLeg], vx, vy, omega):
        self._t = (self._t + dt / self.period) % 1.0
        #print("time : ", self._t)
        for leg, ph in zip(legs, self.PHASE):
            d = self.foot_delta((self._t + ph) % 1.0, self.stroke(leg, vx, vy, omega), leg)
            leg.move_leg_aligned(*d)
            #leg.move_leg_aligned()
            