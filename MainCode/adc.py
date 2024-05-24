import time
#import timeit
import board
import busio
#from cubedetection import CubeDetection
#from displaylib import LCD_driver as LCD
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from multiprocessing import Value

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
voltage_5 = 0 #channel number
voltage_12 = 1 #channel number
ref_v = 3 # empty channel for rev voltage
energy_ws = 0
stop = False

class adc:       
    def get_adc_voltage(channel):
        if channel == 0:
            return chan0.voltage
        elif channel == 1:
            return chan1.voltage
        elif channel == 2:
            return chan2.voltage
        elif channel == 3:
            return chan3.voltage
    
    def get_adc_current(channel):
        if channel == 0:
            chan = chan0
        elif channel == 1:
            chan = chan1
        elif channel == 2:
            chan = chan2
        elif channel == 3:
            chan = chan3
        current = (chan.voltage - 2.45)/0.066
        #current = (0.066/(chan.voltage - 2.45))*0.33
        return current

    def start_measure_power(energy_ret):
        energy_ws = 0
        start = 0
        first = True
        while(True): 
            end = time.time()
            elapsed_time = abs(end - start)
            if first:
                elapsed_time = 0
                first = False
            if adc.get_adc_current(voltage_5) > 0:
                energy_ws = energy_ws + (adc.get_adc_current(voltage_5) * 5 * elapsed_time)
            if adc.get_adc_current(voltage_12) > 0:
                energy_ws = energy_ws + (adc.get_adc_current(voltage_12) * 12 * elapsed_time)
            energy_ret.value = energy_ws
            start = time.time()
            time.sleep(0.02) 


    def test_sensor():
        energy_ws = 0
        start = 0
        first = True
        while(True): 
            end = time.time()
            elapsed_time = abs(end - start)
            if first:
                elapsed_time = 0
                first = False
            if adc.get_adc_current(voltage_5) > 0:
                energy_ws = energy_ws + (adc.get_adc_current(voltage_5) * 5 * elapsed_time)
                #print(adc.get_adc_current(voltage_5))
            if adc.get_adc_current(voltage_12) > 0:
                energy_ws = energy_ws + (adc.get_adc_current(voltage_12) * 12 * elapsed_time)
            print(energy_ws)
            start = time.time()
            time.sleep(0.1) 

adc.test_sensor()