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
lightIN = digitalio.DigitalInOut(board.D17) # Photo Resistor
lightIN.direction = digitalio.Direction.INPUT
laser = digitalio.DigitalInOut(board.D18) # Laser
laser.direction = digitalio.Direction.OUTPUT
run = False

class laser:
    def laser_cannon_deth_sentence():
        global run
        run = True
        while(run):
            laser.value=True #laser off
            time.sleep(0.008)
            laser.value=False #laser on
            time.sleep(0.002)

    def laser_victim():
        end_position
        old_val = lightIN.value
        for i in range(5):
            time.sleep(0.008)
            if (lightIN.value != old_val) & (lightIN.value == False):
                end_position = False
                #print("sensor active")
            elif (lightIN.value == True) & (lightIN.value == old_val):
                #print ("Endposition reached")
                end_position = True
                return True
            old_val = lightIN.value
        return False
    
    def laser_barrier():
        laser.value = True # Laser is off
        if lightIN.value == False: # Check for light pollution
            laser.value = False # Turn on laser
            if lightIN.value == True: # detect laser
                laser.value =True # deactivate laser
                return True
            else:
                laser.value = True
                return False
        return False
    
    def end_laser():
        global run
        run = False