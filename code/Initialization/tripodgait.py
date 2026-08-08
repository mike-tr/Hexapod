
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
    PHASE = (0, 0.5, 0, 0.5, 0, 0.5)
    DUTY = 0.5

    def __init__(self, period=1.0, lift=25.0):
        self.period, self.lift = period, lift
        self._t = 0.0

    def reset(self):
        self._t = 0.0

    def foot_delta(self, phase, offset, stride):
        if phase < self.DUTY:
            u = phase / self.DUTY
            return (offset[0], offset[1] + stride * (0.5 - u), offset[2])
        u = (phase - self.DUTY) / (1 - self.DUTY)
        return (offset[0], offset[1] + stride * (u - 0.5), offset[2] + self.lift * math.sin(math.pi * u))

    def update(self, dt, legs : list[HexLeg], stride):
        self._t = (self._t + dt / self.period) % 1.0
        for leg, ph in zip(legs, self.PHASE):
            d = self.foot_delta((self._t + ph) % 1.0, leg._aligned_home, stride)
            leg.move_leg_aligned(d[0], d[1], d[2])
            #leg.move_leg_aligned()
            