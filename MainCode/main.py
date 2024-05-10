# PREN Gruppe Skogahöf 
# Motorentreiber
#---------------------------------------------------------

import time
import timeit
import board
import busio
import digitalio
from multiprocessing import Process
import adafruit_bus_device.i2c_device as i2c_device
#from adc import adc as adc
from motors import motors
from display import lcddisplay as disp
from laser import laser
from subprocess import check_output


run_once = False

def main():
    ################################# MAIN INIT #################################
    lcd = disp()
    lcd.clear()
    ip = str(check_output(['hostname','-I']))
    ip = ip[2:-3]
    lcd.print("INIT, IP:",lcd.LINE_1)
    lcd.print(f"{ip}",lcd.LINE_2)
    p_init = Process(target=motors.init_position,args=(()))
    p_init.start()
    #motors.init_position()

    from cubedetection import CubeDetection
    
    # Initialize GPIO
    start = digitalio.DigitalInOut(board.D13)
    #start.direction = digitalio.Direction.INPUT
    start_val = start.value

    buzz = digitalio.DigitalInOut(board.D12)
    buzz.direction = digitalio.Direction.OUTPUT

    statled = digitalio.DigitalInOut(board.D6)
    statled.direction = digitalio.Direction.OUTPUT

    p_init.join()
    ############################### MAIN LOOP ###############################
    while(True):
        cubes = ["","","","","","","",""] # yellow, red, blue


        global run_once
        if run_once:
            lcd.print("",lcd.LINE_1)
            lcd.print(f"t={round(t_run,1)}s, E=10Ws",lcd.LINE_2)
            while(not start.value):
                lcd.print("REMOVE CUBES",lcd.LINE_1)
                time.sleep(0.01)
            motors.init_position()

        
        lcd.print("SKOGAHOEF READY PRESS START")

        ################## START RUN ##################


        while(not start.value):
            time.sleep(0.01)

        #lcd.progressbartimed(0,10,1,message="STARTING")
        #lcd.print("STARTING",lcd.LINE_2)
        t_start = time.time()
        statled.value = True
        print(start_val)

        # start img processing
        Process_Cube_Detection = Process(target=CubeDetection.start,args=(()))
        Process_Cube_Detection.start()
        p_lcd = Process(target=lcd.progressbartimed,args=(0,50,25,True,'IMG PROC'))
        p_lcd.start()
        # Wait for Cube Detection Process to end
        Process_Cube_Detection.join()
        p_lcd.kill()
        lcd.clear()
        print(cubes)
        p_lcd = Process(target=lcd.progressbartimed,args=(50,60,3,True,'DROPPING'))
        p_lcd.start()
        motors.drop_cubes(cubes)
        time.sleep(0.05)
        p_lcd.kill()
        lcd.clear()
        p_lcd = Process(target=lcd.progressbartimed,args=(60,80,7,True,'LOWER'))
        p_lcd.start()
        motors.lower_platform()
        p_lcd.kill()
        lcd.clear()
        p_lcd = Process(target=lcd.progressbartimed,args=(80,99,5,True,'CENTER'))
        p_lcd.start()
        motors.center_cubes()
        p_lcd.kill()
        lcd.clear()

        # Accoustic Signal
        t_end = time.time()
        t_run = t_end - t_start
        buzz.value = True
        time.sleep(0.2)
        lcd.progressbar(100,message="FINISHED")
        buzz.value = False
        run = False
        statled.value = False
        run_once = True
############################### END MAIN ###############################

# RUN PROGRAM
main()


