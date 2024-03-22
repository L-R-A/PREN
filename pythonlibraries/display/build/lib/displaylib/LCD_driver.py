import RPi.GPIO as GPIO
import time

# Define GPIO to LCD mapping
LCD_RS = 9
LCD_E  = 10
LCD_D4 = 16
LCD_D5 = 19
LCD_D6 = 20
LCD_D7 = 21

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = 0b1
LCD_CMD = 0b0
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
 
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0001
L_DELAY = 0.002 


def init():
  # Initialise display 
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7
  byte(0x33,LCD_CMD) # 110011 Initialise
  byte(0x32,LCD_CMD) # 110010 Initialise
  byte(0x06,LCD_CMD) # 000110 Cursor move direction
  byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  clear()
  time.sleep(L_DELAY)

def off():
    byte(0b1000,LCD_CMD)
    time.sleep(E_DELAY)

def on():
    byte(0b1100,LCD_CMD)
    time.sleep(E_DELAY)

def cursorON():
    byte(0b1111,LCD_CMD)
    time.sleep(E_DELAY)
def cursorOFF():
    byte(0b1100,LCD_CMD)
    time.sleep(E_DELAY)
def moveCursor(places):
    for i in range(places):
        byte(0b10100,LCD_CMD)
        time.sleep(E_DELAY)
def cursorHome():
    byte(0b10,LCD_CMD)
    time.sleep(L_DELAY)
def clear():
    byte(0x02,LCD_CMD)
    time.sleep(L_DELAY)
    byte(0x01,LCD_CMD) # 000001 Clear display


def byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
 
  GPIO.output(LCD_RS, mode) # RS
 
  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  toggle_enable()
 
  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  toggle_enable()
 
def toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)
 
def string(message,line):
  # Send string to display
 
  message = message.ljust(LCD_WIDTH," ")
 
  byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    byte(ord(message[i]),LCD_CHR)
 
def cleanup():
    GPIO.cleanup()
