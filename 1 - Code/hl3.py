from machine import Pin
from neopixel import NeoPixel 

class color:
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    CYAN = (0, 255, 255)
    GREEN = (0, 255, 0)
    MAGENTA = (255, 0, 255)
    RED = (255, 0, 0)

def init_neopixel():
    return NeoPixel(Pin(0, Pin.OUT), 64)  

class matrix:
    def clear(self, color):
        np = init_neopixel()
        for i in range(0,64):
            np[i] = color
