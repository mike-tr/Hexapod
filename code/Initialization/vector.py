from typing import NamedTuple

class Vec3(NamedTuple):
    x: float
    y: float
    z: float

    def __add__(self, o):
        return Vec3(self.x + o[0], self.y + o[1], self.z + o[2])

    def __sub__(self, o):
        return Vec3(self.x - o[0], self.y - o[1], self.z - o[2])

    def __mul__(self, s):
        return Vec3(self.x * s, self.y * s, self.z * s)

    __rmul__ = __mul__