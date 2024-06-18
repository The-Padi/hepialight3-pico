from machine import Pin
from neopixel import NeoPixel

np_led = 64
gpio_neopixel = 0

class Color:
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    CYAN = (0, 255, 255)
    GREEN = (0, 255, 0)
    MAGENTA = (255, 0, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    RED_DARKER = (153, 0, 0)
    RED_DARK = (204, 0, 0)
    RED_LIGHT = (255, 102, 102)
    RED_LIGHTER = (255, 153, 153)
    BLUE_DARKER = (0, 0, 153)
    BLUE_DARK = (0, 0, 204)
    BLUE_LIGHT = (102, 102, 255)
    BLUE_LIGHTER = (153, 153, 255)
    GREEN_DARKER = (0, 153, 0)
    GREEN_DARK = (0, 204, 0)
    GREEN_LIGHT = (102, 255, 102)
    CYAN_DARK = (0, 204, 204)
    CYAN_LIGHT = (102, 255, 255)
    MAGENTA_DARKER = (153, 0, 153)
    MAGENTA_DARK = (204, 0, 204)
    MAGENTA_LIGHT = (255, 102, 255)
    YELLOW_DARKER = (153, 153, 0)
    YELLOW_DARK = (204, 204, 0)
    YELLOW_LIGHT = (255, 255, 102)
    GRAY_DARK = (64, 64, 64)
    GRAY = (128, 128, 128)
    GRAY_LIGHT = (192, 192, 192)
    ORANGE_DARK = (204, 102, 0)
    ORANGE = (255, 128, 0)
    ORANGE_YELLOW = (255, 204, 0)


def init_neopixel():
    return NeoPixel(Pin(gpio_neopixel, Pin.OUT), np_led)

class matrix:
    def clear(color):
        np = init_neopixel()
        for i in range(np_led):
            np[i] = color
        np.write()