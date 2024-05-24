import time
#import timeit
import board
import busio
import digitalio
#from cubedetection import CubeDetection
from displaylib import LCD_driver as LCD
from adafruit_servokit import ServoKit
from adafruit_motorkit import MotorKit
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from multiprocessing import Process
import adafruit_bus_device.i2c_device as i2c_device
from adafruit_motor import stepper
from subprocess import check_output
i2c = busio.I2C(board.SCL, board.SDA)
hallsens_add = 0x57
hallsens_reg1 = 0x00
hallsens_reg2 = 0x01

try:
    hallsens = i2c_device.I2CDevice(i2c, hallsens_add)
except:
    print("error: could not init hall sensor")
    time.sleep(1)
halldata1 = bytearray(1)
halldata2 = bytearray(1)

class hal:

    def read_value():
        hallsens.write(bytes([hallsens_reg1]))  # Send the register address to read from
        hallsens.readinto(halldata1) 
        hallsens.write(bytes([hallsens_reg2]))  # Send the register address to read from
        hallsens.readinto(halldata2) 
        mask = 0b00000011
        halldata2[0] &= mask
        hall_val = 1024 - (halldata1[0] + (halldata2[0]<<8))
        return hall_val

