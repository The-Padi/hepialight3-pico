from machine import Pin, UART
from neopixel import NeoPixel
from rp2 import PIO, StateMachine, asm_pio
import utime
import framebuf

nb_line = 8
nb_row = 8
gpio_neopixel = 0

np = NeoPixel(Pin(gpio_neopixel, Pin.OUT), nb_line*nb_row)

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

class Direction:
    NORTH = 1
    SOUTH = 2
    EAST = 4
    WEST = 8

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

def Color_convert(Color):
    
    # Handle hex an 0
    if isinstance(Color, int):
        if Color == 0:
            Color = (0, 0, 0)
        else:
            Color = ((Color >> 16) & 0xFF, (Color >> 8) & 0xFF, Color & 0xFF)
    # Handle RGB tuple
    elif isinstance(Color, tuple) and len(Color) == 3:
        pass
    # Error
    else:
        raise ValueError("Color must be an RGB tuple, a hex value, 0 or a valide Color from the Color class")
    
    return Color

class Matrix:
    
    def clear(Color):
        
        # Convert the Color
        Color = Color_convert(Color)
        
        # Set the full screen to the Color
        for i in range(nb_line*nb_row):
            np[i] = Color
        
        # Apply the array
        np.write()
    
    def set_line(line, Color):
        
        # Check line
        if line < 0 or line >= nb_line:
            raise ValueError("Line is out of bound")
        
        # Convert the Color
        Color = Color_convert(Color)
        
        # Set the line to the Color
        for i in range(line*nb_row, (line*nb_row)+nb_row):
            np[i] = Color
        
        # Apply the array
        np.write()
    
    def set_column(column, Color):
        
        # Check column
        if column < 0 or column >= nb_row:
            raise ValueError("Column is out of bound")
        
        # Convert the Color
        Color = Color_convert(Color)
        
        # Set the line to the Color
        for i in range(column, nb_row*nb_line, nb_row):
            np[i] = Color
        
        # Apply the array
        np.write()
    
    def set_led(column, line, Color):
        
        # Check bounds
        if line < 0 or line >= nb_line:
            raise ValueError("Line is out of bound")
        if column < 0 or column >= nb_row:
            raise ValueError("Column is out of bound")
        
        # Convert the Color
        Color = Color_convert(Color)
        
        # Set the specific LED to the Color
        np[line * nb_row + column] = Color
        
        # Apply the array
        np.write()
        
    def get_led(column, line):
        
        # Check bounds
        if line < 0 or line >= nb_line:
            raise ValueError("Line is out of bound")
        if column < 0 or column >= nb_row:
            raise ValueError("Column is out of bound")
        
        # Get the Color of the specific LED
        r, g, b = np[line * nb_row + column]
        
        # Convert to hexadecimal
        hex_Color = (r << 16) | (g << 8) | b
        
        return hex_Color

def rgb_to_rgb565(r, g, b):
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

def rgb565_to_rgb(color):
    r = (color >> 8) & 0xF8
    g = (color >> 3) & 0xFC
    b = (color << 3) & 0xF8
    return (r, g, b)

def framebuffer_to_neopixel(fb):
    for y in range(nb_line):
        for x in range(nb_row):
            color = fb.pixel(x, y)
            np[y * nb_row + x] = rgb565_to_rgb(color)
    np.write()

def show_text(text, color, speed=0.1):
    color_rgb565 = rgb_to_rgb565(*color)
    fb = framebuf.FrameBuffer(bytearray(nb_line * nb_row * 2), nb_row, nb_line, framebuf.RGB565)
    
    for offset in range(len(text) * 8):
        fb.fill(0)
        fb.text(text, -offset, 0, color_rgb565)
        framebuffer_to_neopixel(fb)
        utime.sleep(speed)

class Uart:

    def __init__(self, dir, baudrate=9600, parity=None, bits=8, stop=1):
        
        self.direction = dir

        if (dir == Direction.NORTH):
            self.channel = UART(0, baudrate=baudrate, tx=Pin(12), rx=Pin(13), parity=parity, bits=bits, stop=stop)
        
        elif (dir == Direction.SOUTH):
            self.channel = UART(1, baudrate=baudrate, tx=Pin(8), rx=Pin(9), parity=parity, bits=bits, stop=stop)
        
        elif (dir == Direction.EAST):
            self.tx = StateMachine(0, Uart.uart_tx, freq=8 * baudrate, sideset_base=Pin(14), out_base=Pin(14))
            self.tx.active(1)
            
            self.rx = StateMachine(1, Uart.uart_rx, freq=8 * baudrate, in_base= Pin(15, Pin.IN, Pin.PULL_UP), jmp_pin= Pin(15, Pin.IN, Pin.PULL_UP),)
            self.rx.active(1)
        
        elif (dir == Direction.WEST):
            self.tx = StateMachine(2, Uart.uart_tx, freq=8 * baudrate, sideset_base=Pin(20), out_base=Pin(20))
            self.tx.active(1)
            
            self.rx = StateMachine(3, Uart.uart_rx, freq=8 * baudrate, in_base= Pin(21, Pin.IN, Pin.PULL_UP), jmp_pin= Pin(21, Pin.IN, Pin.PULL_UP),)
            self.rx.active(1)
            
        else:
            raise ValueError("Uart direction does not exist")
    
    @asm_pio(sideset_init=PIO.OUT_HIGH, out_init=PIO.OUT_HIGH, out_shiftdir=PIO.SHIFT_RIGHT)
    def uart_tx():
        # Block with TX deasserted until data available
        pull()
        # Initialize bit counter, assert start bit for 8 cycles
        set(x, 7)  .side(0)       [7]
        # Shift out 8 data bits, 8 execution cycles per bit
        label("bitloop")
        out(pins, 1)              [6]
        jmp(x_dec, "bitloop")
        # Assert stop bit for 8 cycles total (incl 1 for pull())
        nop()      .side(1)       [6]
    
    @asm_pio(in_shiftdir=PIO.SHIFT_RIGHT,)
    def uart_rx():
        # fmt: off
        label("start")
        # Stall until start bit is asserted
        wait(0, pin, 0)
        # Preload bit counter, then delay until halfway through
        # the first data bit (12 cycles incl wait, set).
        set(x, 7)                 [10]
        label("bitloop")
        # Shift data bit into ISR
        in_(pins, 1)
        # Loop 8 times, each loop iteration is 8 cycles
        jmp(x_dec, "bitloop")     [6]
        # Check stop bit (should be high)
        jmp(pin, "good_stop")
        # Either a framing error or a break. Set a sticky flag
        # and wait for line to return to idle state.
        irq(block, 4)
        wait(1, pin, 0)
        # Don't push data if we didn't see good framing.
        jmp("start")
        # No delay before returning to start; a little slack is
        # important in case the TX clock is slightly too fast.
        label("good_stop")
        push(block)
        # fmt: on

    def pio_uart_print(sm, s):
        for c in s:
            sm.put(ord(c))
    
    def send(self, data):
        
        if self.direction == Direction.NORTH or self.direction == Direction.SOUTH:
            self.channel.write(data)
        else:
            Uart.pio_uart_print(self.tx, data)
    
    def sendline(self, data):
        
        if self.direction == Direction.NORTH or self.direction == Direction.SOUTH:
            self.channel.write(data+'\n')
        else:
            Uart.pio_uart_print(self.tx, data+'\n')
    
    def receive(self, length=1):
        data = None
        
        if self.direction == Direction.NORTH or self.direction == Direction.SOUTH:
            while data == None or not len(data) == length:
                data = self.channel.read(length)
                if data is None:
                    utime.sleep(0.1)
        else:
            data = ""
            for i in range(length):
                data += chr(self.rx.get() >> 24)
            
        return data
    
    def receiveline(self):
        data = None
        
        if self.direction == Direction.NORTH or self.direction == Direction.SOUTH:
            while data is None or not data.endswith(b'\n'):
                data = self.channel.readline()
                if data is None:
                    utime.sleep(0.1)
        else:
            data = ""
            while not data.endswith("\n"):
                data += chr(self.rx.get() >> 24)
            
        return data.rstrip()

def christmas():
    
    Color = 0x3
    prime1=439
    prime2=17005013
    
    period = .01
    
    # Balles glissantes
    for r in range(100):
        temp = [[2,5],[1,6],[0,7],[0,7],[0,7],[0,7],[1,6],[2,5]]
        Color = (Color * prime1) % prime2
        # Horizontale et Verticale
        for i in range(8):
            for j in range(temp[i][0],temp[i][-1]+1):
                if (Color&3 == 1):
                    Matrix.set_led(i,j, Color)
                elif (Color&3 == 2):
                    Matrix.set_led(7-i,j, Color)
                else:
                    Matrix.set_led(j,7-i, Color)
            utime.sleep(period)
    
    # Clear the Matrix
    Matrix.clear(0)
    
    # Couleurs clignote
    period = .5
    for r in range(20):
        Color = (Color * prime1) % prime2
        for i in range(8):
            for j in range(8):
                Matrix.set_led(j,i,Color*(i+1)*(j+11))
        utime.sleep(period)
        Matrix.clear(0)
        utime.sleep(period/10)
    
    # Bleu aléatoire
    period = .05
    for r in range(20):
        Color = (Color * prime1) % prime2
        for i in range(8):
            for j in range(8):
                Matrix.set_led(j,i,Color*(i+1)*(j+11) >> 4)
        utime.sleep(period)

    # Couleurs aleatoire
    period = .05
    for r in range(20):
        Color = (Color * prime1) % prime2
        for i in range(8):
            for j in range(8):
                Matrix.set_led(j,i,Color*(i+1)*(j+11))
        utime.sleep(period)

    # Rouge aléatoire
    period = .05
    for r in range(20):
        Color = (Color * prime1) % prime2
        for i in range(8):
            for j in range(8):
                Matrix.set_led(j,i,Color*(i+1)*(j+11))
        utime.sleep(period)

    # Lignes 
    period = .05
    for r in range(20):
        Color = (Color * prime1) % prime2
        for i in range(8):
            Matrix.set_led(Color%8,i,Color*(i+1)*(j+11))
        utime.sleep(period)
        Matrix.clear(0)
        for i in range(8):
            Matrix.set_led(i,Color%8,Color*(i+1)*(j+11))
        utime.sleep(period)
        Matrix.clear(0)
