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
# INSTALLATION -------------------------------------------
#
# sudo apt-get install python-smbus
# sudo apt-get install i2c-tools
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

# initialize i2c
i2c = busio.I2C(board.SCL, board.SDA)

# initialize shields
servoKit = ServoKit(channels=16,address=0x42)
stepperKit = MotorKit(address=0x61,i2c=board.I2C())

# Test Stepper
for i in range(10):
    stepperKit.stepper1.onestep()
    stepperKit.stepper2.onestep()

# Test Servo
servoKit.servo[0].angle = 180
servoKit.continuous_servo[1].throttle = 1
time.sleep(1)
servoKit.continuous_servo[1].throttle = -1
time.sleep(1)
servoKit.servo[0].angle = 0
servoKit.continuous_servo[1].throttle = 0


