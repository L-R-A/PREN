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



class hallsensor:
    i2c = busio.I2C(board.SCL, board.SDA)
    hallsens_add = 0x56
    hallsens_reg = 0x00
    try:
        hallsens = i2c_device.I2CDevice(i2c, hallsens_add)
    except:
        # TODO Print error on display
        #LCD.string(str("I2C Err: HALL"),LCD.LCD_LINE_2)
        time.sleep(3)
    halldata = bytearray(1)
