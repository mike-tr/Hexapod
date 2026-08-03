import math

class IKSystem3:
    def __init__(self, joint1_length, joint2_length, joint3_length):
        # calculate ik, for 3 link chains. We assume that the origin revolves around join1.
        # this class is made to remove redundancies as legs tend to have similar lengths
        self.joint1 = joint1_length
        self.joint2 = joint2_length
        self.joint3 = joint3_length
        self.joint2_sqr = joint2_length**2
        self.joint3_sqr = joint3_length**2

    def angles_from_position(self, x,y,z):
        theta1 = math.atan2(y,x)
        nx = (math.sqrt(x**2 + y**2) - self.joint1)
        nxsqr = nx**2
        print( nx)

        csqr =  nxsqr + z**2 
        c = math.sqrt(csqr)
        t3 = math.acos((self.joint2_sqr + self.joint3_sqr - csqr) / (2 * self.joint2 * self.joint3))
        t2 = math.acos((self.joint2_sqr + csqr - self.joint3_sqr)/(2 * self.joint2 * c))
        t4 = math.asin(z / c)
        theta3 = math.pi - t3
        theta2 = t2 + t4
        return theta1, theta2, theta3


# s = IKSystem3(0.5,1,1.5)
# print(s.angles_from_position(1.1, 0.5, 0.7))

         



    