import time
import sys
import os
import math

# Adds the current folder (Initialization) to the search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pca9685 import PCA9685



MIN_TICK = 102
MAX_TICK = 512
NUM_TICKS = MAX_TICK - MIN_TICK
_PWM_FREQUENCY_HZ = 50
_PWM_OFF_FLAG = 4096

def clamp(n, min_val, max_val):
    return max(min_val, min(n, max_val))

class ServoController:
    """
    Owns the physical hardware. All commands go through here.
    Only ONE instance of this exists.
    """
    def __init__(self):
        self._chips = {
            0x40: PCA9685(0x40),
            0x41: PCA9685(0x41),
        }
        for chip in self._chips.values():
            chip.set_pwm_freq(_PWM_FREQUENCY_HZ)
    
    def get_chip_for_channel(self, channel) -> tuple[PCA9685, int]:
        if not 0 <= channel < 32:
            raise ValueError(f"Channel {channel} out of range (0-31)")
        if channel < 16:
            return self._chips[0x41], channel
        else:
            return self._chips[0x40], channel - 16

# class ServoConfig:
#     def __init__(self, id, rotation_offset, physical_limits):
#         self.id = id
#         self.rotation = rotation_offset
#         self.limits = physical_limits
        

class Servo:
    _chip: PCA9685
    _channel: int
    def __init__(self, controller : ServoController, data):
        self.current_angle = None
        self.servo_id = data["id"]
        self.limits = data["rotation_bounds"]
        self.offset = data["rotation_offset"]
        self._chip, self._channel= controller.get_chip_for_channel(self.servo_id)
            
    def set_angle(self, angle) -> None:
        duty = self._angle_to_duty(angle + self.offset)
        self._chip.set_pwm(self._channel, 0, duty)
        self.current_angle = angle + self.offset
    
    def relax(self) -> None:
        self._chip.set_pwm(self._channel, _PWM_OFF_FLAG , _PWM_OFF_FLAG)
        self.current_angle = None

    def _angle_to_duty(self, angle) -> int:
        if not self.limits[0] <= angle <= self.limits[1]:
            #raise ValueError(f"Angle {angle} out of range [0, 180]")
            print(f"ID: {self.servo_id}, Angle {angle} out of range [{self.limits[0]}, {self.limits[1]}]")
            angle = clamp(angle, self.limits[0], self.limits[1])
            print(f"set angle to {angle}")
        #print(f"ID: {self.servo_id}, angle : {angle}")
        return round((angle / 180) * NUM_TICKS + MIN_TICK)
