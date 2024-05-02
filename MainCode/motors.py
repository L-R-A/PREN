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


release_cube = 180 # angle for cube storage to release cube
turn_magazine = 145 # steps for stepper to turn 90°
platform_move = 2700 # steps for platform to move up or down
try:
    servoKit = ServoKit(channels=16,address=0x42)
except:
    # TODO Print error to Display
    time.sleep(3)
endPosLow = digitalio.DigitalInOut(board.D27)
endPosLow.direction = digitalio.Direction.INPUT 
servo_push1 = servoKit.servo[0]
servo_push2 = servoKit.servo[1]
servo_yellow = servoKit.servo[2]
servo_red = servoKit.servo[3]
servo_blue = servoKit.servo[4]
try:
    stepperKit = MotorKit(address=0x61,i2c=board.I2C())
except:
    # TODO Print error to Display
    print("Init error")
    time.sleep(3)
magazin =  stepperKit.stepper1
platform = stepperKit.stepper2

# Default Positon Cube Push Mechanism    
servo_push1.angle = 0
servo_push2.angle = 0

class motors:
    def start_position():
        # turn to start position with magazin
        # TODO get Hall Sensor value
        hall_val = 255
        mag_counter = 0
        while hall_val < 200:
            if mag_counter < 200:
                magazin.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
            elif mag_counter < 600:
                magazin.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
            mag_counter +=1
        magazin.release()
        
        # reset platform
        while(not endPosLow.value):        
            platform.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        
        for i in range(platform_move):
            platform.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)

        platform.release()