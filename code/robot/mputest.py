"""Minimal MPU-6050 read. Run on the Pi: python3 imu_check.py"""
import time, struct

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus          # python3-smbus package

ADDR        = 0x68
WHO_AM_I    = 0x75
PWR_MGMT_1  = 0x6B
ACCEL_XOUT  = 0x3B
ACCEL_LSB_G = 16384.0                # +/-2g default range
GYRO_LSB    = 131.0                  # +/-250 deg/s default range


def main():
    with SMBus(1) as bus:
        who = bus.read_byte_data(ADDR, WHO_AM_I)
        print(f"WHO_AM_I = 0x{who:02x}", "(MPU-6050)" if who == 0x68 else "(NOT an MPU-6050!)")

        bus.write_byte_data(ADDR, PWR_MGMT_1, 0x00)   # clear sleep bit
        time.sleep(0.1)

        print("\n  ax      ay      az     |a|      gx      gy      gz")
        for _ in range(20):
            raw = bus.read_i2c_block_data(ADDR, ACCEL_XOUT, 14)
            ax, ay, az, _temp, gx, gy, gz = struct.unpack(">7h", bytes(raw))
            ax, ay, az = ax/ACCEL_LSB_G, ay/ACCEL_LSB_G, az/ACCEL_LSB_G
            mag = (ax*ax + ay*ay + az*az) ** 0.5
            print(f"{ax:+7.3f} {ay:+7.3f} {az:+7.3f} {mag:7.3f}  "
                  f"{gx/GYRO_LSB:+7.1f} {gy/GYRO_LSB:+7.1f} {gz/GYRO_LSB:+7.1f}")
            time.sleep(0.1)


if __name__ == "__main__":
    main()