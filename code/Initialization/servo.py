import time
import sys
import os

# Adds the current folder (Initialization) to the search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pca9685 import PCA9685

def map_value(value, from_low, from_high, to_low, to_high):
    """Map a value from one range to another."""
    return (to_high - to_low) * (value - from_low) / (from_high - from_low) + to_low

# print(map_value(90, 0, 180, 500, 2500))

class Servo:
    def __init__(self):
        self.pwm_40 = PCA9685(0x40, debug=True)
        self.pwm_41 = PCA9685(0x41, debug=True)
        # Set the cycle frequency of PWM to 50 Hz
        self.pwm_40.set_pwm_freq(50)
        time.sleep(0.02)
        self.pwm_41.set_pwm_freq(50)
        time.sleep(0.02)

    def set_angle(self, channel, angle):
        duty_cycle = map_value(angle, 0, 180, 500, 2500)
        duty_cycle = map_value(duty_cycle, 0, 20000, 0, 4095)
        if channel < 16:
            self.pwm_41.set_pwm(channel, 0, int(duty_cycle))
        elif 16 <= channel < 32:
            self.pwm_40.set_pwm(channel-16, 0, int(duty_cycle))
    
    def relax(self, channel):
        if channel < 16:
            self.pwm_41.set_pwm(channel, 4096, 4096)
        elif 16 <= channel < 32:
            self.pwm_40.set_pwm(channel-16, 4096, 4096)