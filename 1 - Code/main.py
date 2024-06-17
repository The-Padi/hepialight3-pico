from machine import Pin
from neopixel import NeoPixel
from matrix import matrix
from color import color

pin = Pin(0, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
np = NeoPixel(pin, 64)   # create NeoPixel driver on GPIO0 for 64 pixels

while True:
    matrix.clear(color.RED)