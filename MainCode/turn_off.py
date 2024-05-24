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

class off:
    def turn_off(lcd):
        while(True):
            if start.value:
                time.sleep(3)
                if start.value:
                    print("Power Off")
                    lcd.clear()
                    lcd.print("SHUTTING DOWN",lcd.LINE_1)
                    motors.release()
                    statled.value = True
                    time.sleep(0.1)
                    statled.value = False
                    time.sleep(0.1)
                    statled.value = True
                    time.sleep(0.1)
                    statled.value = False
                    time.sleep(0.1)
                    lcd.clear()
                    cmd = shlex.split("sudo shutdown -h now")
                    subprocess.call(cmd)
            time.sleep(0.01)

