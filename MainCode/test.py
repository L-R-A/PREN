from display import lcddisplay as lcd
import time

lcd = lcd()

time.sleep(0.5)

lcd.print("Dini fetti Mom isch dumm!")

time.sleep(0.5)

for i in range(26):
    lcd.progressbar(4*i)
    
