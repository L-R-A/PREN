# PREN Gruppe Skogahöf 
# Motorentreiber
#---------------------------------------------------------

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
#from adc import adc as adc
from motors import motors

# Global Vars
run = False
run_once = False
lightIN = digitalio.DigitalInOut(board.D17) # Photo Resistor
lightIN.direction = digitalio.Direction.INPUT
energy_wh = 0
end_position = False # for platform -> laser detection
status = 'idle' # for status update and progress on display 
cube_storage = ["yellow","red","blue"] # 3 = dummy


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


        """
        # warn to remove cubes
        if run_once:
            while(not start.value):
                status = 'ready_again'
                time.sleep(0.01)
        
        status = 'preparing'
        """
        motors.start_position()
        while True:
            time.sleep(1)


        
        status = 'ready'

        ################## START RUN ##################
        while(not start.value):
            time.sleep(0.01)
        statled.value = True
        run_once = True

        # start img processing
        status = 'img_proc'
        run = True
        #cubes = CubeDetection.start()
        

         

        print(cubes)
        # cube drop process
        status = 'cube_drop'

        """
        Die Werte 1-8 bezeichnen die Positionen eines Würfels oder einer leeren Stelle in der Konfiguration.
        Die Position 1 spezifiziert die Stelle die auf dem weissen Sektor des Drehtellers, liegt die Positionen 2,
        3, 4 die 3 anderen auf dem Teller liegenden Sektoren im Gegenuhrzeigersinn. Die Positionen 5, 6, 7, 8
        sind diejenigen auf dem 2 Level, i.e. auf einem darunterliegenden Würfel. Ist an der entsprechenden
        Stelle kein Würfel, so ist die Position leer. Position 5 liegt auf 1, 6 auf 2, 7 auf 3 und 8 auf 4.
        """

        # defined cube storages in global list: 0 = yellow, 1 = red, 2 = blue, 3 = dummy
        # Turn forward
        for i in range(0,3,1):
            if cube_storage[0] == cubes[i]:
                servo_yellow.angle = release_cube
            if i <= 2:
                if cube_storage[1] == cubes [i + 1]:
                    servo_red.angle = release_cube
            else:
                if cube_storage[1] == cubes [i - 3]:
                    servo_red.angle = release_cube
            if i <= 1:    
                if cube_storage[2] == cubes[i + 2]:
                    servo_blue.angle = release_cube
            else:
                if cube_storage[2] == cubes[i - 2]:
                    servo_blue.angle = release_cube

            # reset servos
            time.sleep(0.01)
            servo_yellow.angle = 0
            servo_red.angle = 0
            servo_blue.angle = 0

            # turn magazin for 90°
            for i in range(turn_magazine):
                magazin.onestep(direction=stepper.FORWARD, style = stepper.DOUBLE)
            magazin.release()

        # turn backward
        for i in range(7,4,-1):
            if cube_storage[0] == cubes[i]:
                servo_yellow.angle = release_cube
            if i <= 2:
                if cube_storage[1] == cubes [i + 1]:
                    servo_red.angle = release_cube
            else:
                if cube_storage[1] == cubes [i - 3]:
                    servo_red.angle = release_cube
            if i <= 1:    
                if cube_storage[2] == cubes[i + 2]:
                    servo_blue.angle = release_cube
            else:
                if cube_storage[2] == cubes[i - 2]:
                    servo_blue.angle = release_cube

            # reset servos
            time.sleep(0.01)
            servo_yellow.angle = 0
            servo_red.angle = 0
            servo_blue.angle = 0

            # turn magazin for 90°
            for i in range(turn_magazine):
                magazin.onestep(direction=stepper.BACKWARD, style = stepper.DOUBLE)
            magazin.release()

        """
        for i in range(2):
            turnrange = 180
            if(i==0):
                turnrange=160
            servo_yellow.angle = turnrange
            servo_red.angle = turnrange
            servo_blue.angle = turnrange
            time.sleep(0.5)
            servo_yellow.angle = 0
            servo_red.angle = 0
            servo_blue.angle = 0
            time.sleep(0.5)
            if(i==1):
                break
            for j in range(turn_magazine):
                magazin.onestep(direction=stepper.BACKWARD, style = stepper.DOUBLE)
        
        
        for i in range(turn_magazine):
            magazin.onestep(direction=stepper.FORWARD, style = stepper.DOUBLE)
        magazin.release()
        """

        servo_yellow.angle = 0
        servo_red.angle = 0
        servo_blue.angle = 0


        status = 'lower_plattform'
        #platform.onestep(direction=stepper.BACKWARD,style=stepper.DOUBLE)
        
        #for i in range(platform_move-150):
            #platform.onestep(direction=stepper.BACKWARD, style = stepper.DOUBLE)
        platform.release()


        
        while(endPosLow.value):
            if end_position == True:
                break    
            platform.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        platform.release()
       


        status = 'cube_center'
        # When Platform is low enough -> Push cubes together
        servo_push1.angle = 155
        servo_push2.angle = 155
        for i in range(25):
            servo_push1.angle = 155+i
            servo_push2.angle = 155+i
            time.sleep(0.15)
   
        time.sleep(1)    
        servo_push1.angle = 0
        servo_push2.angle = 0

        status = 'finished'
        # Accoustic Signal
        #buzz.value = True
        time.sleep(0.2)
        buzz.value = False
        run = False
        statled.value = False
############################### END MAIN ###############################

# RUN PROGRAM
main()


