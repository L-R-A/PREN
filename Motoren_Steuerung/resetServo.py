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
import pwmio
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
from adafruit_motor import stepper

# Global Vars
run = False

# initialize i2c
i2c = busio.I2C(board.SCL, board.SDA)

hallsens_add = 0x56
hallsens_reg = 0x00
hallsens = i2c_device.I2CDevice(i2c, hallsens_add)    
halldata = bytearray(1)

def laser_cannon_deth_sentence():
    while(True):
        laser = digitalio.DigitalInOut(board.D18) # Laser
        laser.direction = digitalio.Direction.OUTPUT
        
        while(run):
            #current = (0.066/((chan1.voltage/2) - chan0.voltage))*0.33
            laser.value=True
            time.sleep(0.008)
            laser.value=False
            time.sleep(0.002)

def laser_victim():
    while(True):
        lightIN = digitalio.DigitalInOut(board.D17) # Photo Resistor
        lightIN.direction = digitalio.Direction.INPUT
        old_val = lightIN.value
        #timer_prev = time.time_ns()
        sensor = False
        while(run):
            #timer = time.time_ns()
            #if lightIN.value != old_val & (timer - timer_prev) < 8000000:
            time.sleep(0.008)
            if lightIN.value != old_val:
                #timer_prev = timer
                sensor = True
                print("sensor active")
                #time.sleep(0.01)
            elif (lightIN.value == False) & (lightIN.value == old_val) & (sensor == False):
                print("light pollution")
                #sensor = False
            elif (lightIN.value == True) & (lightIN.value == old_val):
                print ("Endposition reached")
                sensor = False
            
            old_val = lightIN.value
            #time.sleep(0.002)          
          
    

def main():
    
    servoKit = ServoKit(channels=16,address=0x42)
    stepperKit = MotorKit(address=0x61,i2c=board.I2C())
    servoKit.servo[4]._pwm_out
        
    # initialize LCD
    LCD.init()

    # Initialize GPIO
    start = digitalio.DigitalInOut(board.D13)
    start.direction = digitalio.Direction.INPUT

    buzz = digitalio.DigitalInOut(board.D12)
    buzz.direction = digitalio.Direction.OUTPUT

    statled = digitalio.DigitalInOut(board.D6)
    statled.direction = digitalio.Direction.OUTPUT

    servoKit.servo[0].angle = 0
    servoKit.servo[1].angle = 0

    Thread_Laser = Thread(target=laser_cannon_deth_sentence,args=(()))
    #Thread_Laser.start()

    Thread_Laser_Victim = Thread(target=laser_victim,args=(()))
    #Thread_Laser_Victim.start()

    ServoValue = 0
    while(True):
        if(start.value):
            if(ServoValue == 0):
                ServoValue = 174
                servoKit.servo[0].angle = ServoValue
                servoKit.servo[1].angle = ServoValue
                LCD.string("UwU", LCD.LCD_LINE_1)   
                for i in range(100):
                    stepperKit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
                for i in range(100):
                    stepperKit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.MICROSTEP)
        
                stepperKit.stepper1.release()

            else:
                ServoValue = 0
                servoKit.servo[0].angle = ServoValue
                servoKit.servo[1].angle = ServoValue 
                LCD.string("^_~",LCD.LCD_LINE_1)
        time.sleep(0.5)
main()


