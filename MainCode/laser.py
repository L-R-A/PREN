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

class laser:
    i2c = busio.I2C(board.SCL, board.SDA)
    lightIN = digitalio.DigitalInOut(board.D17) # Photo Resistor
    lightIN.direction = digitalio.Direction.INPUT

    def laser_cannon_deth_sentence():
        while(True):
            laser = digitalio.DigitalInOut(board.D18) # Laser
            laser.direction = digitalio.Direction.OUTPUT
            
            while(run):
                laser.value=True
                time.sleep(0.008)
                laser.value=False
                time.sleep(0.002)

    def laser_victim():
        while(True):
            global end_position
            old_val = lightIN.value
            sensor = False
            while(run):
                time.sleep(0.008)
                if (lightIN.value != old_val) & (lightIN.value == False):
                    sensor = True
                    end_position = False
                    #print("sensor active")
                elif (lightIN.value == True) & (lightIN.value == old_val):
                    #print ("Endposition reached")
                    sensor = False
                    end_position = True
                old_val = lightIN.value