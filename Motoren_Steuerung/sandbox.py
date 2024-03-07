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
# install Servo-Hat package:
# pip3 install adafruit-circuitpython-servokit
#
# install Stepper-Hat package:
# pip3 install adafruit-circuitpython-motorkit
#
#---------------------------------------------------------

import time
from adafruit_servokit import ServoKit
from adafruit_motorkit import MotorKit

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
servoKit = ServoKit(channels=8)

# Set up Stepper Kit
stepperKit = MotorKit()

stepperKit.motor1.throttle = 1.0
time.sleep(0.5)
stepperKit.motor1.throttle = 0


# Test Servo
servoKit.servo[0].angle = 180
servoKit.continuous_servo[1].throttle = 1
time.sleep(1)
servoKit.continuous_servo[1].throttle = -1
time.sleep(1)
servoKit.servo[0].angle = 0
servoKit.continuous_servo[1].throttle = 0

# Test Stepper
for i in range(100):
    stepperKit.stepper1.onestep()
