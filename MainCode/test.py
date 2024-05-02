from display import lcddisplay as lcd
import time

lcd = lcd()

time.sleep(0.5)

lcd.print("Dini fetti Mom isch dumm!")
time.sleep(0.5)

lcd.print("Dini fetti Mom!", lcd.LINE_2)
time.sleep(0.5)

lcd.progressbar(10)
time.sleep(0.5)
lcd.progressbar(60)
time.sleep(0.5)
lcd.progressbar(75)
time.sleep(0.5)
lcd.progressbar(90)
time.sleep(0.5)
lcd.progressbar(100)
time.sleep(0.5)
    
