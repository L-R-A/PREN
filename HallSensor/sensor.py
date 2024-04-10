# PREN Gruppe Skogahöf 
# Motorentreiber
# 
# USEFULL LINKS ------------------------------------------
# https://pinout.xyz/pinout/i2c
#
# Servo-Hat
# https://cdn-learn.adafruit.com/downloads/pdf/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi.pdf
# 
# Stepper-Hat
# https://docs.circuitpython.org/projects/motorkit/en/latest/
# 
# Stepper Data-Sheet
# https://cdn-shop.adafruit.com/product-files/324/C140-A+datasheet.jpg
#
# ADC ADS1015
# (https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/ads1015-slash-ads1115)
# https://learn.adafruit.com/adafruit-4-channel-adc-breakouts/python-circuitpython
#
# LCD 
# https://github.com/bogdal/rpi-lcd
#
# INSTALLATION -------------------------------------------
# basic Tools:
# sudo apt-get install python-smbus
# sudo apt-get install i2c-tools
# 
# install adc library:
# sudo pip3 install adafruit-circuitpython-ads1x15
#
# install Servo-Hat package:
# sudo pip3 install adafruit-circuitpython-servokit
#
# install Stepper-Hat package:
# sudo pip3 install adafruit-circuitpython-motorkit
#
# install lcd library:
# pip install RPLCD
# 
#---------------------------------------------------------

import time
#import datetime
import board
import busio
import digitalio
#import RPi.GPIO as GPIO
from displaylib import LCD_driver as LCD
from adafruit_servokit import ServoKit
from adafruit_motorkit import MotorKit
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from threading import Thread
import adafruit_bus_device.i2c_device as i2c_device
   

def main():
    # initialize i2c
    i2c = busio.I2C(board.SCL, board.SDA)
    print(i2c.scan())  
    LCD.init()

    hallsens_add = 0x56
    hallsens_reg = 0x00
    hallsens = i2c_device.I2CDevice(i2c, hallsens_add)    
    data = bytearray(1)
    
    while True:
        hallsens.write(bytes([hallsens_reg]))  # Send the register address to read from
        hallsens.readinto(data)   

        print("Magnetic strength: ", 255 - data[0])
        LCD.string("Mag. strength: ", LCD.LCD_LINE_1)    
        LCD.string(str(255 - data[0]), LCD.LCD_LINE_2)

main()








