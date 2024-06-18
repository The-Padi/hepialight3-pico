from machine import Pin
from neopixel import NeoPixel
import utime

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

# use https://goo.gl/gGYfJV to add new chars
__TEXT_DICT = {
    ' ': [],
    'A': [14, 17, 17, 31, 17, 17, 17],
    'B': [15, 17, 17, 31, 17, 17, 15],
    'C': [14, 17, 1, 1, 1, 17, 14],
    'D': [15, 17, 17, 17, 17, 17, 15],
    'E': [31, 1, 1, 15, 1, 1, 31],
    'F': [31, 1, 1, 15, 1, 1, 1],
    'G': [14, 17, 1, 1, 25, 17, 30],
    'H': [17, 17, 17, 31, 17, 17, 17],
    'I': [31, 4, 4, 4, 4, 4, 31],
    'J': [31, 16, 16, 16, 16, 17, 14],
    'K': [17, 17, 9, 7, 9, 17, 17],
    'L': [1, 1, 1, 1, 1, 1, 31],
    'M': [17, 27, 27, 21, 21, 17, 17],
    'N': [17, 19, 21, 21, 25, 17, 17],
    'O': [14, 17, 17, 17, 17, 17, 14],
    'P': [15, 17, 17, 17, 15, 1, 1],
    'Q': [14, 17, 17, 17, 17, 21, 14, 4, 8],
    'R': [15, 17, 17, 15, 9, 17, 17],
    'S': [30, 1, 1, 14, 16, 16, 15],
    'T': [31, 4, 4, 4, 4, 4, 4],
    'U': [17, 17, 17, 17, 17, 17, 14],
    'V': [17, 17, 17, 17, 10, 10, 4],
    'W': [17, 17, 21, 21, 21, 10, 10],
    'X': [17, 17, 10, 4, 10, 17, 17],
    'Y': [17, 10, 4, 4, 4, 4, 4],
    'Z': [31, 16, 8, 4, 2, 1, 31],
    'a': [0, 0, 14, 16, 30, 17, 30],
    'b': [1, 1, 13, 19, 17, 17, 15],
    'c': [0, 0, 14, 17, 1, 17, 14],
    'd': [16, 16, 30, 17, 17, 17, 14],
    'e': [0, 0, 14, 17, 31, 1, 30],
    'f': [24, 4, 30, 4, 4, 4, 31],
    'g': [0, 0, 30, 17, 17, 25, 22, 16, 14],
    'h': [1, 1, 15, 17, 17, 17, 17],
    'i': [4, 0, 7, 4, 4, 4, 31],
    'j': [16, 0, 28, 16, 16, 16, 16, 17, 14],
    'k': [1, 1, 9, 9, 7, 9, 17],
    'l': [7, 4, 4, 4, 4, 4, 31],
    'm': [0, 0, 21, 31, 21, 21, 21],
    'n': [0, 0, 13, 19, 17, 17, 17],
    'o': [0, 0, 14, 17, 17, 17, 14],
    'p': [0, 0, 13, 19, 17, 17, 15, 1, 1],
    'q': [0, 0, 30, 17, 17, 25, 22, 16, 16],
    'r': [0, 0, 27, 6, 2, 2, 15],
    's': [0, 0, 30, 1, 14, 16, 15],
    't': [0, 4, 31, 4, 4, 4, 24],
    'u': [0, 0, 17, 17, 17, 25, 22],
    'v': [0, 0, 17, 17, 10, 10, 4],
    'w': [0, 0, 17, 21, 21, 10, 10],
    'x': [0, 0, 17, 17, 14, 17, 17],
    'y': [0, 0, 17, 17, 10, 10, 4, 4, 3],
    'z': [0, 0, 31, 8, 4, 2, 31],
    '0': [14, 25, 21, 21, 21, 19, 14],
    '1': [4, 7, 4, 4, 4, 4, 31],
    '2': [14, 17, 16, 14, 1, 1, 31],
    '3': [14, 17, 16, 14, 16, 17, 14],
    '4': [8, 12, 10, 9, 31, 8, 8],
    '5': [31, 1, 1, 15, 16, 16, 15],
    '6': [12, 2, 1, 15, 17, 17, 14],
    '7': [31, 16, 8, 4, 2, 2, 2],
    '8': [14, 17, 17, 14, 17, 17, 14],
    '9': [14, 17, 17, 30, 16, 8, 6],
    '.': [0, 0, 0, 0, 0, 4, 4],
    ',': [0, 0, 0, 0, 0, 4, 4, 2],
    ';': [0, 0, 4, 4, 0, 4, 4, 2],
    '?': [14, 17, 16, 12, 0, 4, 4],
    '!': [4, 4, 4, 4, 0, 4, 4],
    '-': [0, 0, 0, 0, 14],
    '_': [0, 0, 0, 0, 0, 0, 31],
    '*': [0, 0, 10, 4, 10],
    '+': [0, 0, 4, 4, 31, 4, 4],
    '/': [16, 16, 8, 4, 4, 2, 2],
    '\\': [2, 2, 4, 8, 8, 16, 16],
    '<': [0, 0, 8, 4, 2, 4, 8],
    '>': [0, 0, 2, 4, 8, 4, 2],
    '#': [10, 10, 31, 10, 31, 10, 10],
    '=': [0, 0, 0, 31, 0, 31],
    '\'': [8, 8, 4],
    '%': [11, 11, 4, 2, 2, 13, 13, 0, 0],
    '&': [6, 1, 1, 6, 5, 9, 22, 0, 0],
    '@': [14, 17, 29, 27, 31, 1, 30, 0, 0],
    '$': [4, 30, 5, 14, 20, 15, 4, 0, 0],
}
    
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
        
    def get_led(column, line):
        
        # Check bounds
        if line < 0 or line >= nb_line:
            raise ValueError("Line is out of bound")
        if column < 0 or column >= nb_row:
            raise ValueError("Column is out of bound")
        
        # Get the color of the specific LED
        r, g, b = np[line * nb_row + column]
        
        # Convert to hexadecimal
        hex_color = (r << 16) | (g << 8) | b
        
        return hex_color

def afficher_texte(text, color, speed):

    # Clear the screen
    matrix.clear(0)

    width = 5
    height = 8
    h_offset = 8
    spacewidth = 2

    def printColumn(step, xpos, text):
        if step < h_offset or step >= h_offset + len(text) * (width + spacewidth):
            char = ' '
            col = 0
        else:
            step -= h_offset
            char = text[step // (width + spacewidth)]
            col = step % (width + spacewidth)
            if char not in __TEXT_DICT:
                char = ' '
        colbit = 1 << col
        charMap = __TEXT_DICT[char]
        for line in range(height):
            colored = len(charMap) > line and charMap[line] & colbit
            matrix.set_led(xpos, line, color if colored else 0)

    for step in range(h_offset + len(text) * (width + spacewidth) + 1):
        for i in range(nb_row):
            printColumn(step + i, i, text)
        utime.sleep(speed)

def christmas():
    
    color = 0x3
    prime1=439
    prime2=17005013

    masque_blanc= 0x0f0f0f   # setup LEDs intensity
    masque_rouge=0x0f0000
    masque_bleu=0x00000f
    
    period = .01
    
    # Balles glissantes
    for r in range(100):
        color = (color * prime1) % prime2
        # horizontale et verticale
        if color&4 == 4:
            for i in range(8):
                temp = (4-int(abs(4.5-i))+1)
                temp = max(3-2*int(temp/2),0)
                for j in range(temp,8-temp):
                    if (color&3 == 0):
                        diagonal=min(int((i+j)),7)
                    elif (color&3 == 1):
                        matrix.set_led(i,j, color&masque_blanc)
                    elif (color&3 == 2):
                        matrix.set_led(7-i,j, color&masque_blanc)
                    else:
                        matrix.set_led(j,7-i, color&masque_blanc)
                utime.sleep(period)

        # Diagonale
        else:
            for k in range(2,9):
                for i in range(k+1):
                    if (4.5-(k-i))**2+(4.5-i)**2 < 5**2:
                        if (color&3 == 0):
                            matrix.set_led((k-i),(i), color&masque_blanc)
                        elif (color&3 == 1):
                            matrix.set_led((i),(k-i), color&masque_blanc)
                        elif (color&3 == 2):
                            matrix.set_led((7-(k-i)),(i), color&masque_blanc)
                        else:
                            matrix.set_led((i),7-(k-i), color&masque_blanc)
                utime.sleep(period)

    
    # Clear the matrix
    matrix.clear(0)
    
    # Couleurs clignote
    period = .5
    for r in range(20):
        color = (color * prime1) % prime2
        for i in range(8):
            for j in range(8):
                matrix.set_led(j,i,color*(i+1)*(j+11) & masque_blanc)
        utime.sleep(period)
        matrix.clear(0)
        utime.sleep(period/10)
    
    # Bleu aléatoire
    period = .05
    for r in range(20):
        color = (color * prime1) % prime2
        for i in range(8):
            for j in range(8):
                matrix.set_led(j,i,color*(i+1)*(j+11) >> 4 & masque_bleu)
        utime.sleep(period)

    # Couleurs aleatoire
    period = .05
    for r in range(10):
        color = (color * prime1) % prime2
        for i in range(8):
            for j in range(8):
                matrix.set_led(j,i,color*(i+1)*(j+11) & masque_blanc)
        utime.sleep(period)

    # Rouge aléatoire
    period = .05
    for r in range(10):
        color = (color * prime1) % prime2
        for i in range(8):
            for j in range(8):
                matrix.set_led(j,i,color*(i+1)*(j+11) & masque_rouge)
        utime.sleep(period)

    # Lignes 
    period = .05
    for r in range(10):
        color = (color * prime1) % prime2
        for i in range(8):
            matrix.set_led(color%8,i,color*(i+1)*(j+11) & masque_blanc)
        utime.sleep(period)
        matrix.clear(0)
        for i in range(8):
            matrix.set_led(i,color%8,color*(i+1)*(j+11) & masque_blanc)
        utime.sleep(period)
        matrix.clear(0)