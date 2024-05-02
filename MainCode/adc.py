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
from adc import adc as adc


stop = False

class adc:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        # initialize ADC
        try:
            ads = ADS.ADS1015(i2c)
        except:
                # TODO print error on Display
                #LCD.string(str("I2C Err: ADC"),LCD.LCD_LINE_2)
                time.sleep(3)
        ads.gain = 2/3
        chan0 = AnalogIn(ads, ADS.P0)
        chan1 = AnalogIn(ads, ADS.P1)
        chan2 = AnalogIn(ads, ADS.P2)
        chan3 = AnalogIn(ads, ADS.P3)
        
    def get_adc_voltage(self, channel):
        if channel == 0:
            return adc.chan0.voltage
        elif channel == 1:
            return adc.chan1.voltage
        elif channel == 2:
            return adc.chan2.voltage
        elif channel == 3:
            return adc.chan3.voltage
    
    def get_adc_current(self, channel):
        if channel == 0:
            chan = adc.chan0
        elif channel == 1:
            chan = adc.chan1
        elif channel == 2:
            chan = adc.chan2
        elif channel == 3:
            chan = adc.chan3
        
        current = (0.066/(2.5 - chan.voltage))*0.33
        return current

    def start_measure_power(self):
        global stop
        stop = False
        energy_ws = 0
        while(not stop):
            time.sleep(0.1)
            energy_ws = energy_ws + (adc.get_adc_current(0) * adc.get_adc_voltage(1) * 0.1)
        return energy_ws
        
    def stop_measure_power(self):
        global stop
        stop = True

