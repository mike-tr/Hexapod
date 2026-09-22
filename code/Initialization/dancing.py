
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

    def __init__(self):
        pass

    def reset(self):
        self._t = 0.0

    def update(self, legs : list[HexLeg], pose : Vec3):

        for leg in legs:
            leg.move_leg_aligned(leg._aligned_home + pose)

            