# PREN Gruppe Skogahöf 
# Motorentreiber
# 
# USEFULL LINKS ------------------------------------------
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
# INSTALLATION -------------------------------------------
#
# sudo apt-get install python-smbus
# sudo apt-get install i2c-tools
# 
# sudo pip3 install adafruit-circuitpython-ads1x15
#
# install Servo-Hat package:
# sudo pip3 install adafruit-circuitpython-servokit
#
# install Stepper-Hat package:
# sudo pip3 install adafruit-circuitpython-motorkit
#
#---------------------------------------------------------

import time
import board
import busio
from adafruit_servokit import ServoKit
from adafruit_motorkit import MotorKit
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

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

# Test ADC
print("A0: {:.2f} V ({}) {:.3f} A".format(chan0.voltage, chan0.value, (0.066/(2.46908 - chan0.voltage))))
print("A1: {:.2f} V ({})".format(chan1.voltage, chan1.value))
print("A2: {:.2f} V ({})".format(chan2.voltage, chan2.value))
print("A3: {:.2f} V ({})".format(chan3.voltage, chan3.value))

# Test Stepper
for i in range(600):
    stepperKit.stepper1.onestep()
    stepperKit.stepper2.onestep()

# Test Servo
servoKit.servo[0].angle = 90
servoKit.continuous_servo[1].throttle = 1
time.sleep(1)
servoKit.continuous_servo[1].throttle = -1
time.sleep(1)
servoKit.servo[0].angle = 0
servoKit.continuous_servo[1].throttle = 0





