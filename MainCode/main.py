# PREN Gruppe Skogahöf 
# Motorentreiber
#---------------------------------------------------------

import time
#import timeit
import board
import busio
import digitalio
from cubedetection import CubeDetection
#from displaylib import LCD_driver as LCD
from multiprocessing import Process
import adafruit_bus_device.i2c_device as i2c_device
#from adc import adc as adc
import display.display
from motors import motors
from display import lcddisplay as disp
from laser import laser

def main():
    ################################# MAIN INIT #################################
    # Initialize GPIO
    start = digitalio.DigitalInOut(board.D13)
    start.direction = digitalio.Direction.INPUT

    buzz = digitalio.DigitalInOut(board.D12)
    buzz.direction = digitalio.Direction.OUTPUT

    statled = digitalio.DigitalInOut(board.D6)
    statled.direction = digitalio.Direction.OUTPUT

    lcd = disp()
    time.sleep(1)
    ############################### MAIN LOOP ###############################
    while(True):
        cubes = ["","","","","","","",""] # yellow, red, blue

        motors.init_position()
        # TODO print Status
        lcd.clear()
        lcd.print("TEST")
        ################## START RUN ##################
        while(not start.value):
            time.sleep(0.01)
        statled.value = True

        # start img processing
        status = 'img_proc'
        run = True

        Process_Cube_Detection = Process(target=CubeDetection.start,args=(()))
        Process_Cube_Detection.start()
        motors.start_position()

        # Wait for Cube Detection Process to end
        Process_Cube_Detection.join()
        # TODO maybe print Cubes to LCD
        print(cubes)
        # TODO print status to LCD
        # cube drop process
        motors.drop_cubes(cubes)
        # TODO print Status
        motors.lower_platform()
        # TODO print Status
        motors.center_cubes()
        # TODO print Status

        # Accoustic Signal
        #buzz.value = True
        time.sleep(0.2)
        buzz.value = False
        run = False
        statled.value = False
############################### END MAIN ###############################

# RUN PROGRAM
main()


