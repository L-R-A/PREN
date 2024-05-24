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
from laser import laser
from hallsensor import hal


release_cube = 180 # angle for cube storage to release cube
turn_magazine = 138 # steps for stepper to turn 90°
platform_move = 3100 # steps for platform to move up or down
drop_time = 0.5
try:
    servoKit = ServoKit(channels=16,address=0x42)
except:
    # TODO Print error to Display
    time.sleep(3)
endPosLow = digitalio.DigitalInOut(board.D27)
endPosLow.direction = digitalio.Direction.INPUT 
servo_push1 = servoKit.servo[0]
servo_push2 = servoKit.servo[1]
servo_yellow = servoKit.servo[3]
servo_red = servoKit.servo[2]
servo_blue = servoKit.servo[4]
yellow = "yellow"
red = "red"
blue = "blue"
cube_storage = ["yellow","red","blue"] # 3 = dummy

try:
    stepperKit = MotorKit(address=0x61,i2c=board.I2C())
except:
    # TODO Print error to Display
    print("Init error")
    time.sleep(3)
magazin =  stepperKit.stepper1
platform = stepperKit.stepper2

# Default Positon Cube Push Mechanism    
#servo_push1.angle = 0
#servo_push2.angle = 0

class motors:
    def init_magazin():
        while hal.read_value() < 1020:
            magazin.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        magazin.release()

    def init_position():  
        servo_push1.angle = 0
        servo_push2.angle = 0
        servo_yellow.angle = 0 
        servo_red.angle = 0
        servo_blue.angle = 0

        # init magazin
        for i in range(50):
            magazin.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
        magazin.release()
        time.sleep(0.5)
        motors.init_magazin()

        # reset platform
        while(not endPosLow.value):        
            platform.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            #platform.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        
        for i in range(platform_move):
            platform.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)

        platform.release()

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
    
    def drop_cubes_new(res):
        # defined cube storages in global list: 0 = yellow, 1 = red, 2 = blue, 3 = dummy
        # Turn forward
        cubes = []
        slot = [0,0,0,0] # number of cubes in slots
        for cube in res:
            cubes.append(cube)
        number_of_cubes = 0
        for i in cubes:
            if i == red or i == yellow or i == blue:
                number_of_cubes += 1
        print(f"number of cubes to drop: {number_of_cubes}")

        for i in range(0,4):
            if i <= 2:
                num_red = i + 1
                num_red_high = i + 5
            else:
                num_red = i - 3
                num_red_high = i - 3
            if i <= 1:
                num_blue = i + 2
                num_blue_high = i + 6
            else:
                num_blue = i - 2 
                num_blue_high = i - 2 
          
            if yellow == cubes[i] and red == cubes[num_red] and blue == cubes[num_blue]:
                print(f"drop yellow, red, blue: {i}")
                servo_yellow.angle = servo_red.angle = servo_blue.angle = release_cube
                time.sleep(drop_time)
                servo_yellow.angle = servo_red.angle = servo_blue.angle = 0
                time.sleep(drop_time)
                slot[i]=slot[i]+1
                slot[num_red]=slot[num_red]+1
                slot[num_blue]=slot[num_blue]+1
                number_of_cubes -= 3
                if number_of_cubes == 0:
                    return
                if yellow == cubes[i+4] and red == cubes[num_red_high] and blue == cubes[num_blue_high]:
                    print(f"drop High yellow, red, blue: {i}")
                    servo_yellow.angle = servo_red.angle = servo_blue.angle = release_cube
                    time.sleep(drop_time)
                    servo_yellow.angle = servo_red.angle = servo_blue.angle = 0
                    time.sleep(drop_time)
                    slot[i]=slot[i]+1
                    slot[num_red]=slot[num_red]+1
                    slot[num_blue]=slot[num_blue]+1
                    number_of_cubes -= 3
                    if number_of_cubes == 0:
                        return
            elif yellow == cubes[i] and red == cubes[num_red]:
                print(f"drop yellow, red: {i}")
                servo_yellow.angle = servo_red.angle  = release_cube
                time.sleep(drop_time)
                servo_yellow.angle = servo_red.angle =  0
                time.sleep(drop_time)
                slot[i]=slot[i]+1
                slot[num_red]=slot[num_red]+1
                number_of_cubes -= 2
                if number_of_cubes == 0:
                    return
                if yellow == cubes[i+4] and red == cubes[num_red_high]:
                    print(f"drop High yellow, red: {i}")
                    servo_yellow.angle = servo_red.angle  = release_cube
                    time.sleep(drop_time)
                    servo_yellow.angle = servo_red.angle =  0
                    time.sleep(drop_time)
                    slot[i]=slot[i]+1
                    slot[num_red]=slot[num_red]+1
                    number_of_cubes -= 2
                    if number_of_cubes == 0:
                        return
            elif yellow == cubes[i] and blue == cubes[num_blue]:
                print(f"drop yellow, blue: {i}")
                servo_yellow.angle = servo_blue.angle = release_cube
                time.sleep(drop_time)
                servo_yellow.angle = servo_blue.angle = 0
                time.sleep(drop_time)
                slot[i]=slot[i]+1
                slot[num_blue]=slot[num_blue]+1
                number_of_cubes -= 2
                if number_of_cubes == 0:
                    return
                if yellow == cubes[i+4] and blue == cubes[num_blue_high]:
                    print(f"drop High yellow, blue: {i}")
                    servo_yellow.angle = servo_blue.angle = release_cube
                    time.sleep(drop_time)
                    servo_yellow.angle = servo_blue.angle = 0
                    time.sleep(drop_time)
                    slot[i]=slot[i]+1
                    slot[num_blue]=slot[num_blue]+1
                    number_of_cubes -= 2
                    if number_of_cubes == 0:
                        return
            elif red == cubes[num_red] and blue == cubes[num_blue]:
                print(f"drop red, blue: {i}")
                servo_red.angle = servo_blue.angle = release_cube
                time.sleep(drop_time)
                servo_red.angle = servo_blue.angle = 0
                time.sleep(drop_time)
                slot[num_red]=slot[num_red]+1
                slot[num_blue]=slot[num_blue]+1
                number_of_cubes -= 2
                if number_of_cubes == 0:
                    return
                if red == cubes[num_red_high] and blue == cubes[num_blue_high]:
                    print(f"drop High red, blue: {i}")
                    servo_red.angle = servo_blue.angle = release_cube
                    time.sleep(drop_time)
                    servo_red.angle = servo_blue.angle = 0
                    time.sleep(drop_time)
                    slot[num_red]=slot[num_red]+1
                    slot[num_blue]=slot[num_blue]+1
                    number_of_cubes -= 2
                    if number_of_cubes == 0:
                        return
            elif yellow == cubes[i]:
                print(f"drop yellow: {i}")
                servo_yellow.angle = release_cube
                time.sleep(drop_time)
                servo_yellow.angle = 0
                time.sleep(drop_time)
                slot[i]=slot[i]+1
                number_of_cubes -= 1
                if number_of_cubes == 0:
                    return
                if yellow == cubes[i+4]:
                    print(f"drop High yellow: {i}")
                    servo_yellow.angle = release_cube
                    time.sleep(drop_time)
                    servo_yellow.angle = 0
                    time.sleep(drop_time)
                    slot[i]=slot[i]+1
                    number_of_cubes -=1
                    if number_of_cubes == 0:
                        return
            elif red == cubes[num_red]:
                print(f"drop red: {i}")
                servo_red.angle = release_cube
                time.sleep(drop_time)
                servo_red.angle = 0
                time.sleep(drop_time)
                slot[num_red]=slot[num_red]+1
                number_of_cubes -= 1
                if number_of_cubes == 0:
                    return
                if red == cubes[num_red_high]:
                    print(f"drop High red: {i}")
                    servo_red.angle = release_cube
                    time.sleep(drop_time)
                    servo_red.angle = 0
                    time.sleep(drop_time)
                    slot[num_red]=slot[num_red]+1
                    number_of_cubes -=1
                    if number_of_cubes == 0:
                        return
            elif blue == cubes[num_blue]:
                print(f"drop blue: {i}")
                servo_red.angle = release_cube
                time.sleep(drop_time)
                servo_red.angle = 0
                time.sleep(drop_time)
                slot[num_blue]=slot[num_blue]+1
                number_of_cubes -= 1
                if number_of_cubes == 0:
                    return
                if blue == cubes[num_blue_high]:
                    print(f"drop High blue: {i}")
                    servo_red.angle = release_cube
                    time.sleep(drop_time)
                    servo_red.angle = 0
                    time.sleep(drop_time)
                    slot[num_blue]=slot[num_blue]+1
                    number_of_cubes -= 1
                    if number_of_cubes == 0:
                        return

            # turn magazin for 90°
            if i < 3:
                for i in range(turn_magazine):
                    magazin.onestep(direction=stepper.FORWARD, style = stepper.DOUBLE)
                magazin.release()

        # check if all slots are full and return
        if slot[0] == slot[1] == slot[2] == slot[3] == 2:
            for i in range(3*turn_magazine):
                magazin.onestep(direction=stepper.BACKWARD, style = stepper.DOUBLE)
            magazin.release()
            return

        # turn backward
        for i in range(7,3,-1):
            if i > 6:
                num_red = i - 3
            else: 
                num_red = i + 1
            if i > 5:
                num_blue = i - 2
            else:
                num_blue = i + 2
            if yellow == cubes[i] and red == cubes[num_red] and blue == cubes[num_blue]:
                print(f"drop yellow, red, blue: {i}")
                servo_yellow.angle = servo_red.angle = servo_blue.angle = release_cube
                time.sleep(drop_time)
                servo_yellow.angle = servo_red.angle = servo_blue.angle = 0
                time.sleep(drop_time)
            elif yellow == cubes[i] and red == cubes[num_red]:
                servo_yellow.angle = servo_red.angle  = release_cube
                time.sleep(drop_time)
                servo_yellow.angle = servo_red.angle =  0
                time.sleep(drop_time)
            elif yellow == cubes[i] and blue == cubes[num_blue]:
                servo_yellow.angle = servo_blue.angle = release_cube
                time.sleep(drop_time)
                servo_yellow.angle = servo_blue.angle = 0
                time.sleep(drop_time)
            elif red == cubes[num_red] and blue == cubes[num_blue]:
                servo_red.angle = servo_blue.angle = release_cube
                time.sleep(drop_time)
                servo_red.angle = servo_blue.angle = 0
                time.sleep(drop_time)
            elif yellow == cubes[i]:
                servo_yellow.angle = release_cube
                time.sleep(drop_time)
                servo_yellow.angle = 0
                time.sleep(drop_time)
            elif red == cubes[num_red]:
                print(f"drop red: {i}")
                servo_red.angle = release_cube
                time.sleep(drop_time)
                servo_red.angle = 0
                time.sleep(drop_time)
            elif blue == cubes[num_blue]:
                servo_red.angle = release_cube
                time.sleep(drop_time)
                servo_red.angle = 0
                time.sleep(drop_time)

            if i > 5:
                # turn magazin for 90°
                for i in range(turn_magazine):
                    magazin.onestep(direction=stepper.BACKWARD, style = stepper.DOUBLE)
                magazin.release()
            if i == 5:
                motors.init_magazin()

    def drop_cubes(res):
        # defined cube storages in global list: 0 = yellow, 1 = red, 2 = blue, 3 = dummy
        # Turn forward
        cubes = []
        slot = [0,0,0,0] # number of cubes in slots
        for cube in res:
            cubes.append(cube)

        for i in range(0,4):
            # drop yellow
            if slot[i] < 2: # check if slot is full
                if yellow == cubes[i]: 
                    print('drop yellow')
                    servo_yellow.angle = release_cube
                    time.sleep(drop_time)
                    servo_yellow.angle = 0
                    time.sleep(drop_time)
                    slot[i] += 1 
                    if yellow == cubes[i+4] and slot[i] < 2: # check if two cubes can be dropped at once
                        servo_yellow.angle = release_cube
                        time.sleep(drop_time)
                        servo_yellow.angle = 0
                        time.sleep(drop_time)
                        slot[i] += 1 
            # drop red 
            if i <= 2:
                if slot[i+1] < 2:
                    if red == cubes [i+1]:
                        print('drop red')
                        servo_red.angle = release_cube
                        time.sleep(drop_time)
                        servo_red.angle = 0
                        time.sleep(drop_time)
                        slot[i+1] += 1 
                        if red == cubes[i+5] and slot[i+1] < 2: 
                            time.sleep(drop_time)
                            servo_red.angle = release_cube
                            time.sleep(drop_time)
                            servo_red.angle = 0
                            slot[i+1] += 1 
            else:
                if slot[i-3] < 2:
                    if red == cubes [i-3]:
                        print('drop red')
                        servo_red.angle = release_cube
                        time.sleep(drop_time)
                        servo_red.angle = 0
                        time.sleep(drop_time)
                        slot[i-3] += 1
                        if red == cubes[i+1] and slot[i-3] < 2: 
                            servo_red.angle = release_cube
                            servo_red.angle = 0
                            slot[i-3] += 1
            # drop blue  
                      
            if i <= 1:
                if slot[i+2] < 2:  
                    if blue == cubes[i + 2]:
                        print('drop blue')
                        servo_blue.angle = release_cube
                        time.sleep(drop_time)
                        servo_blue.angle = 0
                        time.sleep(drop_time)
                        slot[i+2] += 1
                        if blue == cubes[i+6] and  slot[i+2] < 2:
                            servo_blue.angle = release_cube
                            servo_blue.angle = 0
                            slot[i+2] += 1
            else:
                if slot[i-2] < 2:  
                    if blue == cubes[i - 2]:
                        print('drop blue')
                        servo_blue.angle = release_cube
                        time.sleep(drop_time)
                        servo_blue.angle = 0
                        time.sleep(drop_time)
                        slot[i-2] += 1
                        if blue == cubes[i+2] and  slot[i-2] < 2:
                            servo_blue.angle = release_cube
                            servo_blue.angle = 0
                            slot[i-2] += 1
            # turn magazin for 90°
            if i < 4:
                for i in range(turn_magazine):
                    magazin.onestep(direction=stepper.FORWARD, style = stepper.DOUBLE)
                magazin.release()

        # check if all slots are full and return
        if slot[0] == slot[1] == slot[2] == slot[3] == 2:
            for i in range(3*turn_magazine):
                magazin.onestep(direction=stepper.BACKWARD, style = stepper.DOUBLE)
            magazin.release()
            return

        # turn backward
        for i in range(7,3,-1):
            if slot[i-4] < 2:
                if yellow == cubes[i]:
                    print('drop yellow')
                    servo_yellow.angle = release_cube
                    time.sleep(drop_time)
                    servo_yellow.angle = 0
                    time.sleep(drop_time)
                    slot[i-4] += 1
            if i > 6:
                if slot[i-7] < 2:
                    if red == cubes [i - 3]:
                        print('drop red')
                        servo_red.angle = release_cube
                        time.sleep(drop_time)
                        servo_red.angle = 0
                        time.sleep(drop_time)
                        slot[i-7] += 1
            else:
                if slot[i-3] < 2:
                    if red == cubes [i + 1]:
                        print('drop red')
                        servo_red.angle = release_cube
                        time.sleep(drop_time)
                        servo_red.angle = 0
                        time.sleep(drop_time)
                        slot[i-3] += 1
            if i > 5:    
                if slot[i - 6] < 2:
                    if blue == cubes[i - 2]:
                        print('drop blue')
                        servo_blue.angle = release_cube
                        time.sleep(drop_time)
                        servo_blue.angle = 0
                        time.sleep(drop_time)
                        slot[i - 6] += 1
            else:
                if slot[i-2] < 2:
                    if blue == cubes[i + 2]:
                        print('drop blue')
                        servo_blue.angle = release_cube
                        time.sleep(drop_time)
                        servo_blue.angle = 0
                        time.sleep(drop_time)
                        slot[i-2] += 1

            if i > 3:
                # turn magazin for 90°
                for i in range(turn_magazine):
                    magazin.onestep(direction=stepper.BACKWARD, style = stepper.DOUBLE)
                magazin.release()

    def lower_platform():
        #Process_Laser = Process(target=laser.laser_cannon_deth_sentence,args=(()))
        #Process_Laser.start()
        while(not endPosLow.value):
            if laser.laser_barrier():
                platform.release()
                break    
            platform.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        #Process_Laser.kill()
        for i in range(50):
            platform.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
        platform.release()
    
    def center_cubes():
        servo_push1.angle = 155
        servo_push2.angle = 155
        for i in range(15):
            servo_push1.angle = 155+i
            servo_push2.angle = 155+i
            time.sleep(0.15)
   
        time.sleep(0.2)

        servo_push1.angle = 0
        servo_push2.angle = 0
    
    def release_servos():
        platform.release()
        magazin.release()
    
    def test_servos():
        # for i in range 50:
        #     platform.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)

        magazin.release()
        platform.release()
        angle = 180
        servo_yellow.angle = 0 
        servo_red.angle = 0
        servo_blue.angle = 0
        servo_yellow.angle = angle 
        time.sleep(0.5)
        servo_red.angle = angle
        time.sleep(0.5)
        servo_blue.angle = angle
        time.sleep(0.5)
        servo_yellow.angle = 0 
        servo_red.angle = 0
        servo_blue.angle = 0

    def test_hall():
        motors.release_servos()
        motors.init_magazin()
        motors.release_servos()
        cubes = ['red', 'red', 'red', 'yellow', 'yellow', 'yellow', 'blue', 'blue']
        motors.drop_cubes_new(cubes)
