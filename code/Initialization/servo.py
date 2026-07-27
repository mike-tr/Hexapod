import time
import sys
import os

# Adds the current folder (Initialization) to the search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pca9685 import PCA9685


MIN_TICK = 102
MAX_TICK = 512
NUM_TICKS = MAX_TICK - MIN_TICK
_PWM_FREQUENCY_HZ = 50
_PWM_OFF_FLAG = 4096

def _angle_to_duty(angle) -> int:
    if not 0 <= angle <= 180:
        raise ValueError(f"Angle {angle} out of range [0, 180]")
    return round((angle / 180) * NUM_TICKS + MIN_TICK)

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
        
class Servo:
    _chip: PCA9685
    _channel: int
    def __init__(self, controller : ServoController, servo_id):
        self.current_angle = None
        self.servo_id = servo_id
        self._chip, self._channel= controller._resolve_channel(servo_id)
            
    def set_angle(self, angle) -> None:
        duty = _angle_to_duty(angle)
        self._chip.set_pwm(self._channel, 0, duty)
        self.current_angle = angle
    
    def relax(self) -> None:
        self._chip.set_pwm(self._channel, _PWM_OFF_FLAG , _PWM_OFF_FLAG)
        self.current_angle = None