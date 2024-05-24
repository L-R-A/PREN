from display import lcddisplay as lcd
from adafruit_motorkit import MotorKit
import time

lcd = lcd()

time.sleep(0.5)

lcd.print("Dini fetti Mom isch dumm!")
time.sleep(0.5)

lcd.print("Dini fetti Mom!", lcd.LINE_2)
time.sleep(0.5)

lcd.progressbartimed(50, 90, processtime = 3, messageshow = True, message="Test")

    
