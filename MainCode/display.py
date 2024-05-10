# PREN Gruppe Skógahöf 
# LCD - Display
#
#author: Luzian Raphael Aufdenblatten
#---------------------------------------------------------

import time
from displaylib import LCD_driver as LCD

class lcddisplay:
    
    def __init__(self) -> None:
        """
        Initialize LCD on instance creation
        :param self: instance to be manipulated
        """
        LCD.init()
        LCD.string("LCD Initialized", LCD.LCD_LINE_1)  
    
    #define constants for lines   
    LINE_1 = 1
    LINE_2 = 2

    def clear(self):
        """
        Print a string onto the LCD.
        :param self: instance to be manipulated
        """
        LCD.clear()
    
    def print(self, message, line = 0):
        """
        Print a string onto the LCD.
        :param self: instance to be manipulated
        :param message: string of message to be printed
        :param line: integer that defines what lines of LCD are used, 
                     0(default) splits string to fit on both lines, LINE_1 uses first line, LINE_2 uses second line
        """
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

    def progressbar(self, progress = 0, percentage = True):
        """
        Print a progressbar with progess in percent.
        :param self: instance to be manipulated
        :param progress: integer of percentage completed (0 to 100)
        :param percentage : boolean that defines if percentage is printed on line 2 or not (default True)
        """
        progress = progress%101
        progressbar = int(progress/100*16)
        bar = "----------------"
        LCD.string(bar[0:progressbar]+">", LCD.LCD_LINE_1)
        if(percentage):
            LCD.string("Progress: "+str(progress)+"%", LCD.LCD_LINE_2)
        
    
    
    