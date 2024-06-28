import os
import time
import timeit
import board
import shlex
import subprocess
import busio
import digitalio
from multiprocessing import Process, Value
from display import lcddisplay as disp
from motors import motors

start = digitalio.DigitalInOut(board.D13)

statled = digitalio.DigitalInOut(board.D6)
statled.direction = digitalio.Direction.OUTPUT

buzz = digitalio.DigitalInOut(board.D12)
buzz.direction = digitalio.Direction.OUTPUT

class off:
    def turn_off(lcd):
        while(True):
            if start.value:
                time.sleep(3)
                if start.value:
                    print("Power Off")
                    lcd.clear()
                    lcd.print("SHUTTING DOWN",lcd.LINE_1)
                    motors.release_servos()
                    statled.value = True
                    time.sleep(0.1)
                    statled.value = False
                    time.sleep(0.1)
                    statled.value = True
                    time.sleep(0.1)
                    statled.value = False
                    time.sleep(0.1)
                    lcd.clear()
                    buzz.value = True
                    time.sleep(0.2)
                    buzz.value = False
                    time.sleep(0.2)
                    buzz.value = True
                    time.sleep(0.2)
                    buzz.value = False
                    cmd = shlex.split("sudo shutdown -h now")
                    subprocess.call(cmd)
                    time.sleep(10)
            time.sleep(0.01)
    def turn_off_timeout(lcd):
        print("Power Off")
        lcd.clear()
        lcd.print("SHUT DOWN:",lcd.LINE_1)
        lcd.print("CANCEL WITH STRT",lcd.LINE_2)
        counter = time.time()
        shutdown = True
        buzz.value = True
        time.sleep(0.2)
        buzz.value = False        
        while (time.time()-counter) < 20:
            lcd.print(f"SHUT DOWN: {(20-int(time.time()-counter))}",lcd.LINE_1)
            if start.value:
                shutdown = False
                lcd.print("CANCELED",lcd.LINE_2)
                time.sleep(2)
                lcd.clear()
                break
            time.sleep(0.1)
        if shutdown:
            motors.release_servos()
            statled.value = True
            time.sleep(0.1)
            statled.value = False
            time.sleep(0.1)
            statled.value = True
            time.sleep(0.1)
            statled.value = False
            time.sleep(0.1)
            lcd.clear()
            buzz.value = True
            time.sleep(0.2)
            buzz.value = False
            time.sleep(0.2)
            buzz.value = True
            time.sleep(0.2)
            buzz.value = False
            cmd = shlex.split("sudo shutdown -h now")
            subprocess.call(cmd)
            time.sleep(10)


