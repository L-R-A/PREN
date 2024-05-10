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
        LCD.clear()
        time.sleep(0.05)
    
    def print(self, message, line = 0):
        """
        Print a string onto the LCD.
        :param self: instance to be manipulated
        :param message: message to be printed
        :param line: choose which line is to be printed on(default 0)
        """
        #LCD.clear()
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

    def progressbar(self, progress = 0, messageshow = True, message="Progress"):
        """
        Print a progressbar with progess in percent.
        :param self: instance to be manipulated
        :param progress: integer of percentage completed (0 to 100)
        :param messageshow : boolean that defines if process and percentage is printed on line 2 or not (default True)
        :param message : string that defines process that is printed on line 2 or not (default True)
        """
        progress = progress%101
        progressbar = int(progress/100*16)
        bar = "----------------"
        LCD.string(bar[0:progressbar]+">", LCD.LCD_LINE_1)
        if(messageshow):
            LCD.string(str(message)+ ": "+str(progress)+"%", LCD.LCD_LINE_2)
    
    def progressbartimed(self, startprogress = 0, endprogress = 0, processtime = 5, messageshow = True, message="Progress"):
        """
        Print a progressbar with progess in percent.
        :param self: instance to be manipulated
        :param progress: integer of percentage completed (0 to 100)
        :param messageshow : boolean that defines if process and percentage is printed on line 2 or not (default True)
        :param message : string that defines process that is printed on line 2 or not (default True)
        """
        startprogress = startprogress%101
        endprogress = endprogress%101
        bar = "----------------"
        steps = abs(endprogress-startprogress)
        waittime = float(processtime/steps)
        for i in range(steps):
            time.sleep(0.01)
            progress = startprogress+i
            progressbar = int((progress)/100*16)
            LCD.string(bar[0:progressbar]+">", LCD.LCD_LINE_1)
            if(messageshow):
                LCD.string(str(message)+ ": "+str(progress)+"%", LCD.LCD_LINE_2)  
                
            time.sleep(waittime - 0.01)  
        
    
    
    