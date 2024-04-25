# PREN Gruppe Skogahöf 
# Motorentreiber
#---------------------------------------------------------

import time
#import timeit
import datetime
import board
import busio
import pigpio
#import main_with_redundancy
from displaylib import LCD_driver as LCD
from adafruit_servokit import ServoKit
from adafruit_motorkit import MotorKit
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from threading import Thread
import adafruit_bus_device.i2c_device as i2c_device
from adafruit_motor import stepper
from subprocess import check_output

# initialize LCD
LCD.init() # TODO: exception handling

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
run = False
lightIN = 17
pi.set_mode(lightIN,pigpio.INPUT)
energy_wh = 0
end_position = False
status = 'idle'
cube_storage = ["yellow","red","blue"] # 3 = dummy

def display():
    global energy_wh
    global lightIN
    global status
    run_once = False
    display_run = False
    start = 0
    while(True):
        process = 0.0
        LCD.string(str("Skogahof ready"),LCD.LCD_LINE_1)
        # check wifi connection
        wifi_ip = check_output(['hostname', '-I'])
        if not run_once:
            if wifi_ip is None:
                LCD.string(str("WIFI not connected"),LCD.LCD_LINE_2)
            else:
                LCD.string(str("IP: " + str(wifi_ip)),LCD.LCD_LINE_2)
        else:
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
            LCD.string(str(round(process,1) + "% " + str(round(end - start),0) + "s " + str(round(energy_wh,2)) + "Wh"),LCD.LCD_LINE_2)
            if process < 100.0:
                process += 0.15
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
        laser = 18
        pi.set_mode(laser,pigpio.OUTPUT)
        
        while(run):
            pi.write(laser,1)
            time.sleep(0.008)
            pi.write(laser,0)
            time.sleep(0.002)

def laser_victim():
    while(True):
        global end_position
        old_val = pi.read(lightIN)
        sensor = False
        while(run):
            time.sleep(0.008)
            if (pi.read(lightIN) != old_val) & (pi.read(lightIN) == False):
                sensor = True
                end_position = False
                #print("sensor active")
            elif (pi.read(lightIN) == True) & (pi.read(lightIN) == old_val):
                #print ("Endposition reached")
                sensor = False
                end_position = True
            old_val = pi.read(lightIN)

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
    servoKit.servo[4]._pwm_out

    # Initialize GPIO
    start = 13
    pi.set_mode(start,pigpio.INPUT)

    buzz = 12
    pi.set_mode(buzz,pigpio.OUTPUT)

    statled = 6
    pi.set_mode(statled,pigpio.OUTPUT)

    ############################# CREATE THREADS #############################
    Thread_Display = Thread(target=current_measurement,args=((chan0,chan1,chan2,chan3,servoKit)))
    Thread_Display.start()

    Thread_Laser = Thread(target=laser_cannon_deth_sentence,args=(()))
    Thread_Laser.start()

    Thread_Laser_Victim = Thread(target=laser_victim,args=(()))
    Thread_Laser_Victim.start()

    Thread_Display = Thread(target=display,args=(()))
    Thread_Display.start()

    ############################### MAIN LOOP ###############################
    while(True):
        global run
        global end_position
        global status
        global cube_storage
        end_position = False
        status = 'idle'
        cubes = ["","","","","","","",""] # yellow, red, blue
        drop_char = 0 # 4 bits to indicate droping: NAV, blue, red, yellow -> 0001 = yellow drop

        # Default Positon Cube Push Mechanism    
        servo_push1.angle = 0
        servo_push2.angle = 0
        stepperKit.stepper1.release()
        stepperKit.stepper2.release()

        ################## START RUN ##################
        while(not pi.read(start)):
            time.sleep(0.1)
        pi.write(statled,1)

        # start img processing
        status = 'img_proc'
        run = True
        #cubes = exec(open(main_with_redundancy).read())

        # cube drop process
        status = 'cube_drop'

        # defined cube storages in global list: 0 = yellow, 1 = red, 2 = blue, 3 = dummy
        if cube_storage[0] == cubes [0]:
            TODO=0
            



        """
        Die Werte 1-8 bezeichnen die Positionen eines Würfels oder einer leeren Stelle in der Konfiguration.
        Die Position 1 spezifiziert die Stelle die auf dem weissen Sektor des Drehtellers, liegt die Positionen 2,
        3, 4 die 3 anderen auf dem Teller liegenden Sektoren im Gegenuhrzeigersinn. Die Positionen 5, 6, 7, 8
        sind diejenigen auf dem 2 Level, i.e. auf einem darunterliegenden Würfel. Ist an der entsprechenden
        Stelle kein Würfel, so ist die Position leer. Position 5 liegt auf 1, 6 auf 2, 7 auf 3 und 8 auf 4.
        """
        

        """
        for i in range(500):
            stepperKit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
            stepperKit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
        time.sleep(1)
        for i in range(500):
            stepperKit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            stepperKit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            
        stepperKit.stepper1.release()
        stepperKit.stepper2.release()
        """
        status = 'lower_plattform'
        while(end_position == False): 
            for i in range(50):
                stepperKit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
                stepperKit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
            """
            for i in range(50):
                stepperKit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.MICROSTEP)
                stepperKit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.MICROSTEP)
           """
            stepperKit.stepper1.release()
            stepperKit.stepper2.release()
        
        status = 'cube_center'
        # When Platform is low enough -> Push cubes together
        servo_push1.angle = 174
        servo_push2.angle = 174    
        time.sleep(1)    
        servo_push1.angle = 0
        servo_push2.angle = 0

        time.sleep(1)

        # Accoustic Signal
        #pi.write(buzz,1)
        time.sleep(0.2)
        pi.write(buzz,0)
        run = False
        pi.write(statled,0)
############################### END MAIN ###############################

# RUN PROGRAM
main()


