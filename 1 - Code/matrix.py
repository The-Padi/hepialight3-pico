from machine import Pin
from neopixel import NeoPixel
from color import color

pin = Pin(0, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
np = NeoPixel(pin, 64)   # create NeoPixel driver on GPIO0 for 64 pixels

class matrix:
    def clear(self, color):
        for i in range(0,64):
            np[i] = color