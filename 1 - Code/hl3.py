from machine import Pin
from neopixel import NeoPixel

nb_line = 8
nb_row = 8
gpio_neopixel = 0

np = NeoPixel(Pin(gpio_neopixel, Pin.OUT), nb_line*nb_row)

class color:
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
    
def col(r, g, b):
    return (r, g, b)

def color_convert(color):
    
    # Handle hex an 0
    if isinstance(color, int):
        if color == 0:
            color = (0, 0, 0)
        else:
            color = ((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)
    # Handle RGB tuple
    elif isinstance(color, tuple) and len(color) == 3:
        pass
    # Error
    else:
        raise ValueError("Color must be an RGB tuple, a hex value, 0 or a valide color from the color class")
    
    return color

class matrix:
    
    def clear(color):
        
        # Convert the color
        color = color_convert(color)
        
        # Set the full screen to the color
        for i in range(nb_line*nb_row):
            np[i] = color
        
        # Apply the array
        np.write()
    
    def set_line(line, color):
        
        # Check line
        if line < 0 or line >= nb_line:
            raise ValueError("Line is out of bound")
        
        # Convert the color
        color = color_convert(color)
        
        # Set the line to the color
        for i in range(line*nb_row, (line*nb_row)+nb_row):
            np[i] = color
        
        # Apply the array
        np.write()
    
    def set_column(column, color):
        
        # Check column
        if column < 0 or column >= nb_row:
            raise ValueError("Column is out of bound")
        
        # Convert the color
        color = color_convert(color)
        
        # Set the line to the color
        for i in range(column, nb_row*nb_line, nb_row):
            np[i] = color
        
        # Apply the array
        np.write()
    
    def set_led(column, line, color):
        
        # Check bounds
        if line < 0 or line >= nb_line:
            raise ValueError("Line is out of bound")
        if column < 0 or column >= nb_row:
            raise ValueError("Column is out of bound")
        
        # Convert the color
        color = color_convert(color)
        
        # Set the specific LED to the color
        np[line * nb_row + column] = color
        
        # Apply the array
        np.write()
