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

class current_measurement:
    while(True):
        global energy_wh
        loop_time = 0.05
        delta_t = 0
        energy_ws = 0
        while(run):
            current = (0.066/(2.5 - chan0.voltage))*0.33
            delta_t =  delta_t + loop_time
            energy_ws = energy_ws + (current * chan1.voltage * delta_t)
            energy_wh = energy_ws / 60 / 60
            hallsens.write(bytes([hallsens_reg]))  # Send the register address to read from
            hallsens.readinto(halldata) 
            time.sleep(loop_time)  