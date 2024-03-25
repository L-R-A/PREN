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


from displaylib import LCD_driver as LCD
import time
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

#initialize LCD
LCD.init()

LCD.string("CPU ready!", LCD.LCD_LINE_1)
LCD.string("Initialize Tests", LCD.LCD_LINE_2)
time.sleep(1)


# initialize shields
LCD.string("Initialize Servos", LCD.LCD_LINE_1)
LCD.string("...",LCD.LCD_LINE_2)
time.sleep(1)
try:
    servoKit = ServoKit(channels=16,address=0x42)
    stepperKit = MotorKit(address=0x61,i2c=board.I2C())
    LCD.string("Success!",LCD.LCD_LINE_2)
except: 
    LCD.string("ERROR!",LCD.LCD_LINE_2)

# Initialize GPIO
LCD.string("Initialize Stepper", LCD.LCD_LINE_1)
LCD.string("...",LCD.LCD_LINE_2)
time.sleep(1)
try:
    start = digitalio.DigitalInOut(board.D13)
    start.direction = digitalio.Direction.INPUT
    LCD.string("Success!",LCD.LCD_LINE_2)
except: 
    LCD.string("ERROR!",LCD.LCD_LINE_2)



try:
    LCD.string("Test Steppers", LCD.LCD_LINE_1)
    LCD.string("...",LCD.LCD_LINE_2)

    # Test Stepper
    for i in range(400):
            stepperKit.stepper1.onestep()
            stepperKit.stepper2.onestep()

    LCD.string("Success!",LCD.LCD_LINE_2)
    time.sleep(1)


    LCD.string("Test Servos", LCD.LCD_LINE_1)
    LCD.string("...",LCD.LCD_LINE_2)


    # Test Servo
    servoKit.servo[0].angle = 180
    servoKit.servo[1].angle = 180
    servoKit.servo[2].angle = 180
    servoKit.servo[3].angle = 180
    #servoKit.continuous_servo[0].throttle = 1
    #servoKit.continuous_servo[1].throttle = 1
    time.sleep(1)
    #servoKit.continuous_servo[0].throttle = -1
    #servoKit.continuous_servo[1].throttle = -1
    time.sleep(1)
    servoKit.servo[0].angle = 0
    servoKit.servo[1].angle = 0
    servoKit.servo[2].angle = 0
    servoKit.servo[3].angle = 0
    #servoKit.continuous_servo[1].throttle = 0
    time.sleep(1)
    LCD.string("Success!",LCD.LCD_LINE_2)
    time.sleep(1)

except: 
    LCD.string("ERROR",LCD.LCD_LINE_2)

LCD.string("Welcome Back!",LCD.LCD_LINE_1)
LCD.string("Systems nominal!", LCD.LCD_LINE_2)
time.sleep(5)
LCD.string("Skogahof", LCD.LCD_LINE_1)
LCD.string("v0.2.1", LCD.LCD_LINE_2)
LCD.cleanup()
