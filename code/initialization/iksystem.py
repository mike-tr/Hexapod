from __future__ import annotations
import time
import sys
import os
import math

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from vector import Vec3


NORMALIZING_FACTOR = 100
EPS = 1e-3

class IKSystem3:
    def __init__(self, L1, L2, L3):
        # calculate ik, for 3 link chains. We assume that the origin revolves around join1.
        # this class is made to remove redundancies as legs tend to have similar lengths
        self._L1 = L1
        self._L2 = L2
        self._L3 = L3
        #print(L1, L2, L3)
        self._L2_sqr = L2**2
        self._L3_sqr = L3**2
        self._max_reach = (L1 + L2 + L3) / NORMALIZING_FACTOR 

    @property
    def max_reach(self):
        return self._L1 + self._L2 + self._L3

    def angles_from_position_normalized(self, pos : Vec3):
        """Ik by normalized coordinates, x=NORMALIZING_FACTOR means full extension outward.
        """
        # print(x * self.max_reach, y * self.max_reach, z *self.max_reach)
        # print( x**2 + y**2 + z** 2)

        # xn = x / NORMALIZING_FACTOR
        # yn = y / NORMALIZING_FACTOR
        # zn = z / NORMALIZING_FACTOR

        # norm = xn**2 + yn**2 + zn**2
        # print(norm)
        # if norm > 1:
        #     norm = math.sqrt
        #print("pre", pos)
        return self.angles_from_position(pos * self.max_reach)

    def angles_from_position(self, pos):
        #print("after", pos)
        # theta1 the angle for first motor
        # looking at the side view from motor2, (nx,z) is the point out tip should reach in that view.
        # c is the distance between motor2 and the tip.
        theta1 = math.atan2(pos.y, pos.x)
        nx = (math.sqrt(pos.x**2 + pos.y**2) - self._L1)
        nxsqr = nx**2
        #print( nx)

        z = pos.z
        csqr =  nxsqr + z**2 
        c = math.sqrt(csqr)

        c_min = abs(self._L2 - self._L3) + EPS
        c_max = (self._L2 + self._L3) - EPS
        if c > c_max or c < c_min:
            print(f"Target unreachable: distance {c:.2f} > max {self._L2 + self._L3:.2f} or < {abs(self._L2 - self._L3):.2f}")
            c_new = min(max(c, c_min), c_max)
            if c > EPS:
                nx *= c_new / c
                z *= c_new / c
            else:
                nx, z = c_new, 0.0
            c = c_new
            nxsqr = nx * nx
            csqr = nxsqr + z**2
        
        t3 = math.acos((self._L2_sqr + self._L3_sqr - csqr) / (2 * self._L2 * self._L3))
        t2 = math.acos((self._L2_sqr + csqr - self._L3_sqr)/(2 * self._L2 * c))
        t4 = math.atan2(z, nx)
        theta3 = math.pi - t3
        theta2 = t2 + t4
        #print(theta1, theta2, theta3)
        #print(toEuler(theta1), toEuler(theta2), toEuler(theta3))
        return math.degrees(theta1), math.degrees(theta2), math.degrees(theta3)


# s = IKSystem3(0.603, 90, 0.895, 90, 1.215, 45)
# print(s.angles_from_position_normalized(0.7, 0.0, -0.35))
# print(s.angles_from_position(1.1, 0.0, -0.5))

         



    