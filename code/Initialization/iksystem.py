import math

def toEuler(a1):
    return a1 * 180 / math.pi 


class IKSystem3:
    def __init__(self, L1, angle1, L2, angle2, L3, angle3):
        # calculate ik, for 3 link chains. We assume that the origin revolves around join1.
        # this class is made to remove redundancies as legs tend to have similar lengths
        self.L1 = L1
        self.L2 = L2
        self.L3 = L3
        self.L2_sqr = L2**2
        self.L3_sqr = L3**2
        self.angle1 = angle1
        self.angle2 = angle2
        self.angle3 = angle3
        self.max_reach = L1 + L2 + L3

    def angles_from_position_normalized(self, x, y, z):
        """Ik by normalized coordinates, x=1.0 means full extension outward.
        """
        print(x * self.max_reach, y * self.max_reach, z *self.max_reach)
        print( x**2 + y**2 + z** 2)
        return self.angles_from_position(x * self.max_reach, y * self.max_reach, z *self.max_reach)

    def angles_from_position(self, x,y,z):
        theta1 = math.atan2(y,x)
        nx = (math.sqrt(x**2 + y**2) - self.L1)
        nxsqr = nx**2
        print( nx)

        csqr =  nxsqr + z**2 
        c = math.sqrt(csqr)
        t3 = math.acos((self.L2_sqr + self.L3_sqr - csqr) / (2 * self.L2 * self.L3))
        t2 = math.acos((self.L2_sqr + csqr - self.L3_sqr)/(2 * self.L2 * c))
        t4 = math.asin(z / c)
        theta3 = math.pi - t3
        theta2 = t2 + t4
        print(theta1, theta2, theta3)
        print(toEuler(theta1), toEuler(theta2), toEuler(theta3))
        return (theta1 * 180) / math.pi + self.angle1, (theta2 * 180) / math.pi + self.angle2, (theta3 * 180) / math.pi + self.angle3


# s = IKSystem3(0.0, 90, 1, 90, 1.5, 45)
# print(s.angles_from_position_normalized(0.7, 0.0, -0.35))
# print(s.angles_from_position(1.1, 0.0, -0.5))

         



    