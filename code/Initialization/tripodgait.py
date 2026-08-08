
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

    def __init__(self, period=1.0, lift=25.0):
        self.period, self.lift = period, lift
        self._t = 0.0

    def reset(self):
        self._t = 0.0

    def foot_delta(self, phase, stride, leg : HexLeg):
        print("phase :", phase)
        if phase < self.DUTY:
            u = phase / self.DUTY
            return (leg._aligned_home[0], leg._aligned_home[1] + stride * (0.5 - u), leg._aligned_home[2])
        u = (phase - self.DUTY) / (1 - self.DUTY)
        return (leg._aligned_home[0] + leg.orientation * 25 * math.sin(math.pi * u), leg._aligned_home[1] + stride * (u - 0.5), leg._aligned_home[2] + self.lift * math.sin(math.pi * u))

    def update(self, dt, legs : list[HexLeg], stride):
        self._t = (self._t + dt / self.period) % 1.0
        print("time : ", self._t)
        for leg, ph in zip(legs, self.PHASE):
            d = self.foot_delta((self._t + ph) % 1.0, stride, leg)
            leg.move_leg_aligned(d[0], d[1], d[2])
            #leg.move_leg_aligned()
            