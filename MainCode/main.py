# PREN Gruppe Skogahöf 
# Motorentreiber
#---------------------------------------------------------

import time
#import timeit
import board
import busio
import digitalio
#from cubedetection import CubeDetection
#from displaylib import LCD_driver as LCD
from multiprocessing import Process
import adafruit_bus_device.i2c_device as i2c_device
#from adc import adc as adc
import display.display
from motors import motors
import display
from laser import laser

# Global Vars
run = False
run_once = False
lightIN = digitalio.DigitalInOut(board.D17) # Photo Resistor
lightIN.direction = digitalio.Direction.INPUT
energy_wh = 0
end_position = False # for platform -> laser detection
status = 'idle' # for status update and progress on display 


def main():
    ################################# MAIN INIT #################################
    # Initialize GPIO
    start = digitalio.DigitalInOut(board.D13)
    start.direction = digitalio.Direction.INPUT

    buzz = digitalio.DigitalInOut(board.D12)
    buzz.direction = digitalio.Direction.OUTPUT

    statled = digitalio.DigitalInOut(board.D6)
    statled.direction = digitalio.Direction.OUTPUT

    ############################### MAIN LOOP ###############################
    while(True):
        global run 
        global status
        global cube_storage
        end_position = False
        status = 'idle'
        cubes = ["","","","","","","",""] # yellow, red, blue

        motors.init_position()
        # TODO print Status
        #disp.print('ready')
        
        ################## START RUN ##################
        while(not start.value):
            time.sleep(0.01)
        statled.value = True

        # start img processing
        status = 'img_proc'
        run = True

        Process_Cube_Detection = Process(target=CubeDetection.start,args=(()))
        Process_Cube_Detection.start()
        #cubes = CubeDetection.start()
        motors.start_position()

        # Wait for Cube Detection Process to end
        Process.join()
        # TODO maybe print Cubes to LCD
        print(cubes)
        # TODO print status to LCD
        #status = 'cube_drop'

        Process_Laser = Process(target=laser.laser_cannon_deth_sentence,args=(()))
        Process_Laser.start()
        
        # cube drop process
        motors.drop_cubes(cubes)
        # TODO print Status
        #status = 'lower_plattform'
        motors.lower_platform()
        # TODO print Status
        #status = 'cube_center'
        motors.center_cubes()
        # TODO print Status
        #status = 'finished'
        # Accoustic Signal
        #buzz.value = True
        time.sleep(0.2)
        buzz.value = False
        run = False
        statled.value = False
############################### END MAIN ###############################

# RUN PROGRAM
main()


