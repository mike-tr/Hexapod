from typing import NamedTuple
import math

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

    def __truediv__(self, s):
        return Vec3(self.x / s, self.y / s, self.z / s)

    def lengthSquared(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def rotate_inv(self, rz_deg, ry_deg, rx_deg):
        cz, sz = math.cos(math.radians(rz_deg)), math.sin(math.radians(rz_deg))
        cy, sy = math.cos(math.radians(ry_deg)), math.sin(math.radians(ry_deg))
        cx, sx = math.cos(math.radians(rx_deg)), math.sin(math.radians(rx_deg))

        # undo rz first
        x1 = self.x * cz + self.y * sz
        y1 = -self.x * sz + self.y * cz
        # then ry
        x = x1 * cy - self.z * sy
        z1 = x1 * sy + self.z * cy
        # then rx
        y = y1 * cx + z1 * sx
        z = -y1 * sx + z1 * cx
        return Vec3(x, y, z)

    def rotate(self, rz_deg, ry_deg, rx_deg):
        # Convert to radians
        rz = math.radians(rz_deg)
        ry = math.radians(ry_deg)
        rx = math.radians(rx_deg)

        # Compute sin,cos per rotation
        cz, sz = math.cos(rz), math.sin(rz)
        cy, sy = math.cos(ry), math.sin(ry)
        cx, sx = math.cos(rx), math.sin(rx)

        #Old code, after combining all rotation in one go, that one has more operations...
        # x = self.x * cz * cy + self.y * (cz * sy * sx - sz * cx) + self.z * (cz * sy * cx + sz * sx)
        # y = self.x * sz * cy + self.y * (sz * sy * sx + cz * cx) + self.z * (sz * sy * cx - cz * sx)
        # z = - self.x * sy + self.y * cy * sx + self.z * cy * cx

        # Apply rx first (rotate yz around the x axis)
        yr = self.y * cx - self.z * sx
        zr = self.y * sx + self.z * cx

        # Apply ry (rotate xz around the y axis)
        xp = self.x * cy + zr * sy
        z = - self.x * sy + zr * cy

        # Apply rz (rotate xy around the z axis)
        x = xp * cz - yr * sz
        y = xp * sz + yr * cz
        return Vec3(x,y,z)
    __rmul__ = __mul__