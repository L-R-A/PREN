from displaylib import LCD_driver as LCD
import time


LCD.init()

try: 
    # Send some test
    LCD.cursorON()
    LCD.string("Test of the 1st Line",LCD.LCD_LINE_1)
    LCD.string("Second Line",LCD.LCD_LINE_2)
    LCD.cursorHome()
    while True:
        
        LCD.moveCursor(1)
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    LCD.off()


