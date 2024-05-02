# PREN Gruppe Skogahöf 
# Display
#
#author: Luzian Aufdenblatten
#---------------------------------------------------------

import time
from displaylib import LCD_driver as LCD


class lcddisplay:
    def __init__(self) -> None:
        LCD.init()
        LCD.string("LCD Initialized", LCD.LCD_LINE_1)  
         
    LINE_1 = 1
    LINE_2 = 2
        
    def clear(self):
        LCD.clear()
    
    def print(self, message, line = 0):
        LCD.clear()
        time.sleep(0.01)
        match(line):
            case 0:
                if(len(message)>16):
                    LCD.string(message[0:15], LCD.LCD_LINE_1)
                    LCD.string(message[15:31], LCD.LCD_LINE_2)
                else:
                    LCD.string(message, LCD.LCD_LINE_1)
            case 1:
                LCD.string(message[0:15], LCD.LCD_LINE_1)
            case 2:
                LCD.string(message[0:15], LCD.LCD_LINE_2)

    def progressbar(self, progress = 0):
        progressbar = int(progress/100*16)
        bar = "-------------------"
        LCD.string(bar[0:progressbar]+">", LCD.LCD_LINE_1)
        LCD.string("Progress: "+str(progress)+"%", LCD.LCD_LINE_2)
        
    
    
    