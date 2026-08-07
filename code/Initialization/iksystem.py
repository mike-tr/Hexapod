import math

NORMALIZING_FACTOR = 100

class IKSystem3:
    def __init__(self, L1, angle1, L2, angle2, L3, angle3):
        # calculate ik, for 3 link chains. We assume that the origin revolves around join1.
        # this class is made to remove redundancies as legs tend to have similar lengths
        self._L1 = L1
        self._L2 = L2
        self._L3 = L3
        self._L2_sqr = L2**2
        self._L3_sqr = L3**2
        self._angle1 = angle1
        self._angle2 = angle2
        self._angle3 = angle3
        self._max_reach = (L1 + L2 + L3) / NORMALIZING_FACTOR 

    def angles_from_position_normalized(self, x, y, z):
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
        
        return self._angles_from_position(x * self._max_reach, y * self._max_reach, z *self._max_reach)

    def angles_from_position(self, x,y,z):
        # theta1 the angle for first motor
        # looking at the side view from motor2, (nx,z) is the point out tip should reach in that view.
        # c is the distance between motor2 and the tip.
        theta1 = math.atan2(y,x)
        nx = (math.sqrt(x**2 + y**2) - self._L1)
        nxsqr = nx**2
        #print( nx)

        csqr =  nxsqr + z**2 
        c = math.sqrt(csqr)
        if c > (self._L2 + self._L3):
            raise ValueError(f"Target unreachable: distance {c:.2f} > max {self._L2 + self._L3:.2f}")
        
        if c < abs(self._L2 - self._L3):
            raise ValueError(f"Target too close: distance {c:.2f} < min {abs(self._L2 - self._L3):.2f}")
        
        t3 = math.acos((self._L2_sqr + self._L3_sqr - csqr) / (2 * self._L2 * self._L3))
        t2 = math.acos((self._L2_sqr + csqr - self._L3_sqr)/(2 * self._L2 * c))
        t4 = math.atan2(z, nx)
        theta3 = math.pi - t3
        theta2 = t2 + t4
        #print(theta1, theta2, theta3)
        #print(toEuler(theta1), toEuler(theta2), toEuler(theta3))
        return math.degrees(theta1) + self._angle1, math.degrees(theta2) + self._angle2, math.degrees(theta3) + self._angle3


# s = IKSystem3(0.603, 90, 0.895, 90, 1.215, 45)
# print(s.angles_from_position_normalized(0.7, 0.0, -0.35))
# print(s.angles_from_position(1.1, 0.0, -0.5))

         



    