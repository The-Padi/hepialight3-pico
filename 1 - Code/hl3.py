from machine import Pin
from neopixel import NeoPixel

np_led = 64
gpio_neopixel = 0

class color:
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    CYAN = (0, 255, 255)
    GREEN = (0, 255, 0)
    MAGENTA = (255, 0, 255)
    RED = (255, 0, 0)

def init_neopixel():
    return NeoPixel(Pin(gpio_neopixel, Pin.OUT), np_led)

class matrix:
    def clear(color):
        np = init_neopixel()
        for i in range(np_led):
            np[i] = color
        np.write()