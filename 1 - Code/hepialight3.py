from machine import Pin
from neopixel import NeoPixel
import time

pin = Pin(0, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
np = NeoPixel(pin, 64)   # create NeoPixel driver on GPIO0 for 64 pixels

while True:
    for j in range(3):
        for i in range(0,64):
            if j == 0:
                np[i] = (255, 0, 0)
            elif j == 1:
                np[i] = (0, 255, 0)
            elif j == 2:
                np[i] = (0, 0, 255)
            np.write()