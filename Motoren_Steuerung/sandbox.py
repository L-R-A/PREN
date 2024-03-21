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
# https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/ads1015-slash-ads1115
#
#
# INSTALLATION -------------------------------------------
#
# sudo apt-get install python-smbus
# sudo apt-get install i2c-tools
# sudo pip install adafruit-ads1x15
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
import Adafruit_ADS1x15
from adafruit_servokit import ServoKit
from adafruit_motorkit import MotorKit

# initialize i2c
i2c = busio.I2C(board.SCL, board.SDA)

# initialize ADC
#adc = Adafruit_ADS1x15.ADS1015(address=0x48, bus=1)
adc = Adafruit_ADS1x15.ADS1015()
GAIN = 1
adc.start_adc(0,gain=GAIN)

# initialize shields
servoKit = ServoKit(channels=16,address=0x42)
stepperKit = MotorKit(address=0x61,i2c=board.I2C())

# Test ADC
print('Reading ADS1x15 channel 0 for 5 seconds...')
start = time.time()
while (time.time() - start) <= 5.0:
    # Read the last ADC conversion value and print it out.
    value = adc.get_last_result()
    # WARNING! If you try to read any other ADC channel during this continuous
    # conversion (like by calling read_adc again) it will disable the
    # continuous conversion!
    print('Channel 0: {0}'.format(value))
    # Sleep for half a second.
    time.sleep(0.5)
# Stop continuous conversion.  After this point you can't get data from get_last_result!
adc.stop_adc()

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





