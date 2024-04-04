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

# Global Vars
run = False

def current_measurement(chan0,chan1,chan2,chan3):
    while(True):
        loop_time = 0.05
        delta_t = 0
        energy_ws = 0
        #print_timer = 0.2
        while(run):
            current = (0.066/(2.5 - chan0.voltage))*0.33
            #current = (0.066/((chan1.voltage/2) - chan0.voltage))*0.33
            delta_t =  delta_t + loop_time
            energy_ws = energy_ws + (current * chan1.voltage * delta_t)
            energy_wh = energy_ws / 60 / 60
            #if(delta_t >= print_timer):
            #    print("{:.3f} A {:.3f} Wh".format(current, energy_wh)) # *0.35 korrektur Offset aus Vergleich mit Messgerät
            #    print_timer = print_timer + 0.2
            print("{:.3f} A {:.3f} Wh".format(current, energy_wh)) # *0.35 korrektur Offset aus Vergleich mit Messgerät
            LCD.string("{:.3f} A {:.3f} Wh".format(current, energy_wh),LCD.LCD_LINE_1)
            time.sleep(loop_time)
        
    

def main():
    # initialize i2c
    i2c = busio.I2C(board.SCL, board.SDA)

    # initialize ADC
    ads = ADS.ADS1015(i2c)
    ads.gain = 2/3
    chan0 = AnalogIn(ads, ADS.P0)
    chan1 = AnalogIn(ads, ADS.P1)
    chan2 = AnalogIn(ads, ADS.P2)
    chan3 = AnalogIn(ads, ADS.P3)

    # initialize shields
    servoKit = ServoKit(channels=16,address=0x42)
    stepperKit = MotorKit(address=0x61,i2c=board.I2C())

    # initialize LCD
    LCD.init()

    # Initialize GPIO
    start = digitalio.DigitalInOut(board.D13)
    start.direction = digitalio.Direction.INPUT

    # create Threads
    Thread1 = Thread(target=current_measurement,args=((chan0,chan1,chan2,chan3)))
    Thread1.start()

    # Endless Main Loop
    while(True):
        global run

        # wait for start button
        while(not start.value):
            time.sleep(0.1)

        run = True

        # Test ADC
        
        #print("A0: {:.2f} V ({}) {:.3f} A".format(chan0.voltage, chan0.value, (0.066/(2.46908 - chan0.voltage))))
        #print("A0: {:.2f} V ({}) {:.3f} A".format(chan0.voltage, chan0.value, (0.066/(2.5 - chan0.voltage))*0.33)) # *0.35 korrektur Offset aus Vergleich mit Messgerät
        #print("A1: {:.2f} V ({})".format(chan1.voltage, chan1.value))
        #print("A2: {:.2f} V ({})".format(chan2.voltage, chan2.value))
        #print("A3: {:.2f} V ({})".format(chan3.voltage, chan3.value))

        # Test Stepper
        for i in range(400):
            stepperKit.stepper1.onestep()
            stepperKit.stepper1.onestep()
            stepperKit.stepper2.onestep()

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
        run = False

# RUN PROGRAM
main()


