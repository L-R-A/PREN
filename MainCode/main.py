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

# initialize LCD
LCD.init() # TODO: exception handltime.sleep(0.5)

# initialize i2c
i2c = busio.I2C(board.SCL, board.SDA)
hallsens_add = 0x56
hallsens_reg = 0x00
try:
    hallsens = i2c_device.I2CDevice(i2c, hallsens_add)
except:
    LCD.string(str("I2C Err: HALL"),LCD.LCD_LINE_2)
    time.sleep(3)
halldata = bytearray(1)

# Global Vars
pi = pigpio.pi()
#pi = pigpio.pi()
run = False
run_once = False
lightIN = digitalio.DigitalInOut(board.D17) # Photo Resistor
lightIN.direction = digitalio.Direction.INPUT
energy_wh = 0
end_position = False # for platform -> laser detection
status = 'idle' # for status update and progress on display 
cube_storage = ["yellow","red","blue"] # 3 = dummy
release_cube = 180 # angle for cube storage to release cube
turn_magazine = 145 # steps for stepper to turn 90°
platform_move = 2700 # steps for platform to move up or down

def display():
    global energy_wh
    global lightIN
    global status
    global run_once
    display_run = False
    start = 0
    while(True):
        process = 0.0
        # check wifi connection
        wifi_ip = check_output(['hostname', '-I'])
        if not run_once:
            LCD.string(str("Skogahof ready"),LCD.LCD_LINE_1)
            if wifi_ip is None:
                LCD.string(str("WIFI not connected"),LCD.LCD_LINE_2)
            else:
                LCD.string(str("IP: " + str(wifi_ip)),LCD.LCD_LINE_2)
        else:
            if status == 'ready_again':
                LCD.string(str("rem CUBES + Strt"),LCD.LCD_LINE_1)
            elif status == 'preparing':
                LCD.string(str("Preparing..."),LCD.LCD_LINE_1)
            elif status == 'ready':
                LCD.string(str("Skogahof ready"),LCD.LCD_LINE_1)
            LCD.string(str("t: " + str(round(prev_time,1)) + "s E: " + str(round(prev_energy,1)) + "Wh"),LCD.LCD_LINE_2)
        display_run = False
        
        while(run):
            # init run
            run_once = True
            if display_run == False:
                start = time.time()
                prev_time = 0
                prev_energy = 0
                display_run = True

            # update status on display line 1
            if status == 'img_proc':
                LCD.string(str("IMG PROCESSING"),LCD.LCD_LINE_1)
            if status == 'cube_drop':
                LCD.string(str("PLACING CUBES"),LCD.LCD_LINE_1)
            if status == 'lower_plattform':
                LCD.string(str("LOWER PLATFORM"),LCD.LCD_LINE_1)
            if status == 'cube_center':
                LCD.string(str("CENTRALIZE CUBES"),LCD.LCD_LINE_1)
                
            # update status on display line 2
            LCD.string(str(str(round(process,1)) + "% " + str(round(end - start),1) + "s " + str(round(energy_wh,2)) + "Wh"),LCD.LCD_LINE_2)
            if process < 100.0:
                process += 0.8
            prev_energy = energy_wh
            end = time.time()
            time.sleep(0.2) # run loop delay time
        
        # time claculation
        if run_once:
            prev_time = end - start
        time.sleep(0.5) # idle delay
    

def current_measurement(chan0,chan1,chan2,chan3,servoKit):
    while(True):
        global energy_wh
        loop_time = 0.05
        delta_t = 0
        energy_ws = 0
        while(run):
            current = (0.066/(2.5 - chan0.voltage))*0.33
            delta_t =  delta_t + loop_time
            energy_ws = energy_ws + (current * chan1.voltage * delta_t)
            energy_wh = energy_ws / 60 / 60
            hallsens.write(bytes([hallsens_reg]))  # Send the register address to read from
            hallsens.readinto(halldata) 
            time.sleep(loop_time)  

def laser_cannon_deth_sentence():
    while(True):
        laser = digitalio.DigitalInOut(board.D18) # Laser
        laser.direction = digitalio.Direction.OUTPUT
        
        while(run):
            laser.value=True
            time.sleep(0.008)
            laser.value=False
            time.sleep(0.002)

def laser_victim():
    while(True):
        global end_position
        old_val = lightIN.value
        sensor = False
        while(run):
            time.sleep(0.008)
            if (lightIN.value != old_val) & (lightIN.value == False):
                sensor = True
                end_position = False
                #print("sensor active")
            elif (lightIN.value == True) & (lightIN.value == old_val):
                #print ("Endposition reached")
                sensor = False
                end_position = True
            old_val = lightIN.value

def main():
    ################################# MAIN INIT #################################
    # initialize ADC
    try:
        ads = ADS.ADS1015(i2c)
    except:
        LCD.string(str("I2C Err: ADC"),LCD.LCD_LINE_2)
        time.sleep(3)
    ads.gain = 2/3
    chan0 = AnalogIn(ads, ADS.P0)
    chan1 = AnalogIn(ads, ADS.P1)
    chan2 = AnalogIn(ads, ADS.P2)
    chan3 = AnalogIn(ads, ADS.P3)

    # initialize shields
    try:
        servoKit = ServoKit(channels=16,address=0x42)
    except:
        LCD.string(str("I2C Err: SERVO"),LCD.LCD_LINE_2)
        time.sleep(3)
    servo_push1 = servoKit.servo[0]
    servo_push2 = servoKit.servo[1]
    servo_yellow = servoKit.servo[2]
    servo_red = servoKit.servo[3]
    servo_blue = servoKit.servo[4]
    try:
        stepperKit = MotorKit(address=0x61,i2c=board.I2C())
    except:
        LCD.string(str("I2C Err: STEPPER"),LCD.LCD_LINE_2)
        time.sleep(3)
    magazin =  stepperKit.stepper1
    platform = stepperKit.stepper2
    
    #servoKit.servo[4]._pwm_out

    # Initialize GPIO
    start = digitalio.DigitalInOut(board.D13)
    start.direction = digitalio.Direction.INPUT

    buzz = digitalio.DigitalInOut(board.D12)
    buzz.direction = digitalio.Direction.OUTPUT

    statled = digitalio.DigitalInOut(board.D6)
    statled.direction = digitalio.Direction.OUTPUT

    endPosLow = digitalio.DigitalInOut(board.D22)
    endPosLow.direction = digitalio.Direction.INPUT 

    ############################# CREATE THREADS #############################
    Process_Display = Process(target=current_measurement,args=((chan0,chan1,chan2,chan3,servoKit)))
    Process_Display.start()

    Process_Laser = Process(target=laser_cannon_deth_sentence,args=(()))
    Process_Laser.start()

    Process_Laser_Victim = Process(target=laser_victim,args=(()))
    Process_Laser_Victim.start()

    Process_Display = Process(target=display,args=(()))
    Process_Display.start()
    ############################### MAIN LOOP ###############################
    while(True):
        global run
        global end_position
        global status
        global cube_storage
        global run_once
        end_position = False
        status = 'idle'
        cubes = ["","","","","","","",""] # yellow, red, blue

        # Default Positon Cube Push Mechanism    
        servo_push1.angle = 0
        servo_push2.angle = 0

        # warn to remove cubes
        if run_once:
            while(not start.value):
                status = 'ready_again'
                time.sleep(0.01)
        
        status = 'preparing'

        # turn to start position with magazin
        hall_val = 255 - halldata[0]
        mag_counter = 0
        while hall_val < 200:
            if mag_counter < 200:
                magazin.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
            elif mag_counter < 600:
                magazin.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
            mag_counter +=1
        magazin.release()

        # reset platform
        while(endPosLow.value):        
            platform.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        
        for i in range(platform_move):
            platform.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)

        platform.release()
        
        status = 'ready'

        ################## START RUN ##################
        while(not start.value):
            time.sleep(0.01)
        statled.value = True

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


        servo_yellow.angle = 0
        servo_red.angle = 0
        servo_blue.angle = 0


        status = 'lower_plattform'
        
        for i in range(platform_move-150):
            platform.onestep(direction=stepper.BACKWARD, style = stepper.DOUBLE)
        magazin.release()


        
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


