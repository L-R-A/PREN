# PREN Gruppe Skogahöf 
# Motorentreiber
#---------------------------------------------------------

import time
import timeit
import board
import busio
import digitalio
from multiprocessing import Process, Value
import adafruit_bus_device.i2c_device as i2c_device
from adc import adc
from motors import motors
from display import lcddisplay as disp
from laser import laser
from subprocess import check_output
from turn_off import off
from hallsensor import hal


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
    energy = Value('f',0)
    turn_off = Process(target=off.turn_off,args=(lcd,))
    turn_off.start()

    from cubedetection import CubeDetection
    
    # Initialize GPIO
    start = digitalio.DigitalInOut(board.D13)

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
            lcd.print(f"{round(t_run,1)}s, {round(energy.value,1)}Ws",lcd.LINE_2)
            while(not start.value):
                lcd.print("REMOVE CUBES",lcd.LINE_1)
                time.sleep(0.01)
            motors.init_position()

        
        lcd.print("SKOGAHOEF READY PRESS START")

        ################## START RUN ##################


        while(not start.value):
            time.sleep(0.05)

        while(start.value):
            time.sleep(0.05)

        #lcd.progressbartimed(0,10,1,message="STARTING")
        #lcd.print("STARTING",lcd.LINE_2)
        t_start = time.time()
        statled.value = True
        # start power measurement
        p_adc = Process(target=adc.start_measure_power,args=(energy,))
        p_adc.start()

        # start img processing
        p_lcd = Process(target=lcd.progressbartimed,args=(0,50,25,True,'IMG PROC'))
        p_lcd.start()
        cubes = CubeDetection.start()
        p_lcd.kill()
        lcd.clear()
        print(cubes)
        p_lcd = Process(target=lcd.progressbartimed,args=(50,60,3,True,'DROPPING'))
        p_lcd.start()
        motors.drop_cubes_new(cubes)
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
        p_adc.kill()
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





