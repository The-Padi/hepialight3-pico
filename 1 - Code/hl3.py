from machine import Pin, UART, I2C, SPI
from neopixel import NeoPixel
from rp2 import PIO, StateMachine, asm_pio
import utime
import time
import framebuf
import gc

nb_line = 8
nb_row = 8
gpio_neopixel = 0

np = NeoPixel(Pin(gpio_neopixel, Pin.OUT), nb_line*nb_row)
fb = framebuf.FrameBuffer(bytearray(nb_line * nb_row * 2), nb_row, nb_line, framebuf.RGB565)
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400_000)
spi = SPI(0, 12_000_000, bits=8, sck=Pin(18), mosi=Pin(19), miso=Pin(16))

p4 = Pin(4, Pin.IN, Pin.PULL_UP)
p22 = Pin(22, Pin.OUT)
p26 = Pin(26, Pin.OUT, value=1)
cs = Pin(17, mode=Pin.OUT, value=1)

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

COLOR_MAP = {
    'R': Color.RED,
    'G': Color.GREEN,
    'B': Color.BLUE,
    'C': Color.CYAN,
    'M': Color.MAGENTA,
    'Y': Color.YELLOW,
    'W': Color.WHITE,
    '.': Color.BLACK
}

class Direction:
    NORTH = 1
    SOUTH = 2
    EAST = 4
    WEST = 8
    FRONT = 16
    BACK = 32
    
class Position:
    NORTH_WEST = 1
    NORTH_EAST = 2
    SOUTH_WEST = 4
    SOUTH_EAST = 8

def Color_convert(color):
    """Convert an input color into a RGB tuple

    Args:
        color (hex, Color, tuple): Input color to convert

    Raises:
        ValueError: Input color is not supported

    Returns:
        tuple: Valid RGB color
    """
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
        raise ValueError("Color must be an RGB tuple, a hex value, 0 or a valide Color from the Color class")
    
    return color

class Matrix:
    
    def clear(color):
        """Set a single color to the entire LED matrix

        Args:
            Color (hex, Color, tuple): Color to apply
        """
        # Convert the Color
        color = Color_convert(color)
        
        # Set the full screen to the Color
        for i in range(nb_line*nb_row):
            np[i] = color
        
        # Apply the array
        np.write()
    
    def set_line(line, color):
        """Set an entire line of LED to a single color

        Args:
            line (int): The line to set
            color (hex, Color, tuple): Color to apply

        Raises:
            ValueError: Input line is out of the LED matrix
        """
        # Check line
        if line < 0 or line >= nb_line:
            raise ValueError("Line is out of bound")
        
        # Convert the Color
        color = Color_convert(color)
        
        # Set the line to the Color
        for i in range(line*nb_row, (line*nb_row)+nb_row):
            np[i] = color
        
        # Apply the array
        np.write()
    
    def set_column(column, color):
        """Set an entire column of LED to a single color

        Args:
            column (int): The column to set
            color (hex, Color, tuple): Color to apply

        Raises:
            ValueError: Input column is out of the LED matrix
        """
        # Check column
        if column < 0 or column >= nb_row:
            raise ValueError("Column is out of bound")
        
        # Convert the Color
        color = Color_convert(color)
        
        # Set the line to the Color
        for i in range(column, nb_row*nb_line, nb_row):
            np[i] = color
        
        # Apply the array
        np.write()
    
    def set_led(column, line, color):
        """Set a specific LED to a specific color

        Args:
            column (int): Column of the LED
            line (int): Line of the LED
            color (hex, Color, tuple): Color to apply

        Raises:
            ValueError: Input line is out of the LED matrix
            ValueError: Input column is out of the LED matrix
        """
        # Check bounds
        if line < 0 or line >= nb_line:
            raise ValueError("Line is out of bound")
        if column < 0 or column >= nb_row:
            raise ValueError("Column is out of bound")
        
        # Convert the Color
        color = Color_convert(color)
        
        # Set the specific LED to the Color
        np[line * nb_row + column] = color
        
        # Apply the array
        np.write()
        
    def get_led(column, line):
        """Get the current color of a specific LED of the matrix

        Args:
            column (int): Column of the LED
            line (int): Line of the LED

        Raises:
            ValueError: Input line is out of the LED matrix
            ValueError: Input column is out of the LED matrix

        Returns:
            hex: Value of the color of the LED
        """
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

def set_img(img):
    """Display a full matrix of colors

    Args:
        img (str): Multi-line string representing the image to be displayed, where each character corresponds to a color code defined in COLOR_MAP

    Raises:
        ValueError: The image is empty
        ValueError: The image is too small for the screen
        ValueError: The image is too big for the screen
    """
    if not img:
        raise ValueError("Image cannot be empty")
    
    arr = [COLOR_MAP[c] for c in img if c in COLOR_MAP]
    
    if len(arr) < nb_line * nb_row:
        raise ValueError(f"Image too small for screen ({len(arr)} pixels for a {nb_line}x{nb_row} screen)")
    elif len(arr) > nb_line * nb_row:
        raise ValueError(f"Image too large for screen ({len(arr)} pixels for a {nb_line}x{nb_row} screen)")
    
    for y in range(nb_line):
        for x in range(nb_row):
            Matrix.set_led(x, y, arr[y * nb_row + x])
            

def rgb_to_rgb565(r, g, b):
    """Convert an RGB color to RGB565 format

    Args:
        r (int): The red component of the color (0-255)
        g (int): The green component of the color (0-255)
        b (int): The blue component of the color (0-255)

    Returns:
        int: The RGB565 representation of the color
    """
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)


def rgb565_to_rgb(color):
    """Convert an RGB565 color to RGB format

    Args:
        color (int): The RGB565 color value

    Returns:
        tuple: A tuple (r, g, b) representing the red, green, and blue components of the color, each in the range 0-255
    """
    r = (color >> 8) & 0xF8
    g = (color >> 3) & 0xFC
    b = (color << 3) & 0xF8
    return (r, g, b)

def framebuffer_to_neopixel(fb):
    """Convert a framebuffer to NeoPixel format and send it to the NeoPixel strip

    Args:
        fb (Framebuffer): The framebuffer object containing pixel data

    """
    for y in range(nb_line):
        for x in range(nb_row):
            color = fb.pixel(x, y)
            np[y * nb_row + x] = rgb565_to_rgb(color)
    np.write()

def show_text(text, color, speed=0.1):
    """Display scrolling text on an LED matrix using a framebuffer

    Args:
        text (str): The text to be displayed
        color (hex, Color, tuple): The color of the text
        speed (float, optional): The speed at which the text scrolls. Defaults to 0.1 seconds per frame
    """
    
    # Convert the Color
    color = Color_convert(color)
    
    color_rgb565 = rgb_to_rgb565(*color)
    
    for offset in range(nb_row + (len(text) * 8)):
        fb.fill(0)
        fb.text(text, nb_row-offset, 0, color_rgb565)
        framebuffer_to_neopixel(fb)
        gc.collect()
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
        """Send data through the appropriate channel based on the direction

        Args:
            data (str or bytes): The data to be sent
        """
        if self.direction == Direction.NORTH or self.direction == Direction.SOUTH:
            self.channel.write(data)
        else:
            Uart.pio_uart_print(self.tx, data)

    
    def sendline(self, data):
        """Send data with a newline character through the appropriate channel based on the direction

        Args:
            data (str): The data to be sent
        """
        if self.direction == Direction.NORTH or self.direction == Direction.SOUTH:
            self.channel.write(data+'\n')
        else:
            Uart.pio_uart_print(self.tx, data+'\n')
    
    def receive(self, length=1):
        """Receive data from the appropriate channel based on the direction

        Args:
            length (int, optional): The number of bytes to read // Defaults to 1

        Returns:
            str or bytes: The data received
        """
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
        """Receive a line of data from the appropriate channel based on the direction

        Returns:
            str: The line of data received, stripped of any trailing newline characters.
        """
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
    
class Accel:
    
    def init():
        """_summary_
        """
        i2c.writeto_mem(0x1d, 0x20, b'\x57')
    
    def get_x():
        """_summary_

        Returns:
            _type_: _description_
        """
        buf = i2c.readfrom_mem(0x1d, 0xa8, 2)
        x = ((buf[0] & 0xff) | ((buf[1] & 0xff) << 8)) / 16384
        if x > 2:
            x = x - 4
        return x
    
    def get_y():
        """_summary_

        Returns:
            _type_: _description_
        """
        buf = i2c.readfrom_mem(0x1d, 0xaa, 2)
        y = ((buf[0] & 0xff) | ((buf[1] & 0xff) << 8)) / 16384
        if y > 2:
            y = y - 4
        return y
        
    def get_z():
        """_summary_

        Returns:
            _type_: _description_
        """
        buf = i2c.readfrom_mem(0x1d, 0xac, 2)
        z = ((buf[0] & 0xff) | ((buf[1] & 0xff) << 8)) / 16384
        if z > 2:
            z = z - 4
        return z
        
    def facing(side):
        """_summary_

        Args:
            side (_type_): _description_

        Returns:
            _type_: _description_
        """
        z = Accel.get_z()
        if side == Direction.FRONT:
            if z < 0:
                return True
            else:
                return False
        elif side == Direction.BACK:
            if z < 0:
                return False
            else:
                return True
        else:
            return False
    
    def tilting(dir):
        """_summary_

        Args:
            dir (_type_): _description_

        Returns:
            _type_: _description_
        """
        if dir == Direction.NORTH or dir == Direction.SOUTH:
            x = Accel.get_x()
            if dir == Direction.NORTH:
                if x > 0.03:
                    return False
                elif x < -0.03:
                    return True
            else:
                if x > 0.03:
                    return True
                elif x < -0.03:
                    return False
        elif dir == Direction.EAST or dir == Direction.WEST:
            y = Accel.get_y()
            if dir == Direction.EAST:
                if y > 0.03:
                    return False
                elif y < -0.03:
                    return True
            else:
                if y > 0.03:
                    return True
                elif y < -0.03:
                    return False
                
class Touch:
    
    callback = None
    
    @classmethod
    def attach(cls, cb):
        """_summary_

        Args:
            cb (function): _description_
        """
        cls.callback = cb

    @classmethod   
    def detach(cls):
        """_summary_
        """
        cls.callback = None
        
    @classmethod    
    def callback_do(cls, *args, **kwargs):
        """_summary_
        """
        if cls.callback:
            cls.callback(*args, **kwargs)
            
    def init():
        """_summary_
        """
        i2c.writeto_mem(0x38, 0xa4, b'\x00')
    
    def read(pos):
        """_summary_

        Args:
            pos (_type_): _description_

        Returns:
            _type_: _description_
        """
        buf = i2c.readfrom_mem(0x38, 0x03, 4)
        flag = buf[0] >> 6
        x = ((buf[0] & 0x0f) << 8) | (buf[1] & 0xff)
        y = ((buf[2] & 0x0f) << 8) | (buf[3] & 0xff)
        if flag == 2:
            if x < 120 and y < 160:
                if pos == Position.SOUTH_EAST:
                    return True
                else:
                    return False
            elif x >= 120 and y < 160:
                if pos == Position.SOUTH_WEST:
                    return True
                else:
                    return False
            elif x < 120 and y >= 160:
                if pos == Position.NORTH_EAST:
                    return True
                else:
                    return False
            elif x >= 120 and y >= 160:
                if pos == Position.NORTH_WEST:
                    return True
                else:
                    return False
                
    def compute_pos(x, y):
        """_summary_

        Args:
            x (_type_): _description_
            y (_type_): _description_

        Returns:
            _type_: _description_
        """
        if x < 120 and y < 160:
            return Position.SOUTH_EAST
        elif x >= 120 and y < 160:
            return Position.SOUTH_WEST
        elif x < 120 and y >= 160:
            return Position.NORTH_EAST
        elif x >= 120 and y >= 160:
            return Position.NORTH_WEST  

    def read_pos():
        """_summary_

        Returns:
            _type_: _description_
        """
        buf = i2c.readfrom_mem(0x38, 0x03, 4)
        x = ((buf[0] & 0x0f) << 8) | (buf[1] & 0xff)
        y = ((buf[2] & 0x0f) << 8) | (buf[3] & 0xff)
        return x, y
    
    def touch_cb(pos):
        """_summary_

        Args:
            pos (_type_): _description_
        """
        if pos == Position.NORTH_WEST:
            Matrix.clear(0)
            for i in range(4):
                for j in range(4):
                    Matrix.set_led(i, j, Color.WHITE)
        elif pos == Position.NORTH_EAST:
            Matrix.clear(0)
            for i in range(4):
                for j in range(4):
                    Matrix.set_led(i + 4, j, Color.RED)
        elif pos == Position.SOUTH_WEST:
            Matrix.clear(0)
            for i in range(4):
                for j in range(4):
                    Matrix.set_led(i, j + 4, Color.GREEN)
        else:
            Matrix.clear(0)
            for i in range(4):
                for j in range(4):
                    Matrix.set_led(i + 4, j + 4, Color.BLUE)
            
    def handler():
        """_summary_
        """
        x, y = Touch.read_pos()
        pos = Touch.compute_pos(x, y)
        Touch.callback_do(pos)
        
class Lcd:
    
    def write_cmd(cmd):
        """_summary_

        Args:
            cmd (_type_): _description_
        """
        p26.off()
        spi.write(cmd)
        
    def write_data(data):
        """_summary_

        Args:
            data (_type_): _description_
        """
        p26.on()
        spi.write(data)
        
    def init():
        """_summary_
        """
        Lcd.write_cmd(b'\x01')
        time.sleep_ms(5)

        Lcd.write_cmd(b'\x11')
        time.sleep_ms(120)

        Lcd.write_cmd(b'\xCF')
        Lcd.write_data(b'\x00')
        Lcd.write_data(b'\x83')
        Lcd.write_data(b'\x30')

        Lcd.write_cmd(b'\xED')
        Lcd.write_data(b'\x64')
        Lcd.write_data(b'\x03')
        Lcd.write_data(b'\x12')
        Lcd.write_data(b'\x81')

        Lcd.write_cmd(b'\xE8')
        Lcd.write_data(b'\x85')
        Lcd.write_data(b'\x01')
        Lcd.write_data(b'\x79')

        Lcd.write_cmd(b'\xCB')
        Lcd.write_data(b'\x39')
        Lcd.write_data(b'\x2C')
        Lcd.write_data(b'\x00')
        Lcd.write_data(b'\x34')
        Lcd.write_data(b'\x02')

        Lcd.write_cmd(b'\xF7')
        Lcd.write_data(b'\x20')

        Lcd.write_cmd(b'\xEA')
        Lcd.write_data(b'\x00')
        Lcd.write_data(b'\x00')


        Lcd.write_cmd(b'\xC1')
        Lcd.write_data(b'\x11')

        Lcd.write_cmd(b'\xC5')
        Lcd.write_data(b'\x34')
        Lcd.write_data(b'\x3D')

        Lcd.write_cmd(b'\xC7')
        Lcd.write_data(b'\xC0')

        Lcd.write_cmd(b'\x36')
        Lcd.write_data(b'\x08')

        Lcd.write_cmd(b'\x3A')
        Lcd.write_data(b'\x55')

        Lcd.write_cmd(b'\xB1')
        Lcd.write_data(b'\x00')
        Lcd.write_data(b'\x1D')

        Lcd.write_cmd(b'\xB6')
        Lcd.write_data(b'\x0A')
        Lcd.write_data(b'\xA2')
        Lcd.write_data(b'\x27')
        Lcd.write_data(b'\x00')

        Lcd.write_cmd(b'\xb7')
        Lcd.write_data(b'\x07')


        Lcd.write_cmd(b'\xF2')
        Lcd.write_data(b'\x08')

        Lcd.write_cmd(b'\x26')
        Lcd.write_data(b'\x01')


        Lcd.write_cmd(b'\xE0')
        Lcd.write_data(b'\x1f')
        Lcd.write_data(b'\x1a')
        Lcd.write_data(b'\x18')
        Lcd.write_data(b'\x0a')
        Lcd.write_data(b'\x0f')
        Lcd.write_data(b'\x06')
        Lcd.write_data(b'\x45')
        Lcd.write_data(b'\x87')
        Lcd.write_data(b'\x32')
        Lcd.write_data(b'\x0a')
        Lcd.write_data(b'\x07')
        Lcd.write_data(b'\x02')
        Lcd.write_data(b'\x07')
        Lcd.write_data(b'\x05')
        Lcd.write_data(b'\x00')

        Lcd.write_cmd(b'\xE1')
        Lcd.write_data(b'\x00')
        Lcd.write_data(b'\x25')
        Lcd.write_data(b'\x27')
        Lcd.write_data(b'\x05')
        Lcd.write_data(b'\x10')
        Lcd.write_data(b'\x09')
        Lcd.write_data(b'\x3a')
        Lcd.write_data(b'\x78')
        Lcd.write_data(b'\x4d')
        Lcd.write_data(b'\x05')
        Lcd.write_data(b'\x18')
        Lcd.write_data(b'\x0d')
        Lcd.write_data(b'\x38')
        Lcd.write_data(b'\x3a')
        Lcd.write_data(b'\x1f')

        Lcd.write_cmd(b'\x11')
        time.sleep_ms(120)
        Lcd.write_cmd(b'\x29')
        time.sleep_ms(50)
        
    def set_window(x, y, width, height):
        """_summary_

        Args:
            x (_type_): _description_
            y (_type_): _description_
            width (_type_): _description_
            height (_type_): _description_
        """
        Lcd.write_cmd(b'\x2a');
        Lcd.write_data(((x >> 8) & 0xff).to_bytes(1, 'big'));
        Lcd.write_data((x & 0xff).to_bytes(1, 'big'));
        Lcd.write_data((((x + width - 1) >> 8) & 0xff).to_bytes(1, 'big'));
        Lcd.write_data(((x + width - 1) & 0xff).to_bytes(1, 'big'));

        Lcd.write_cmd(b'\x2b');
        Lcd.write_data(((y >> 8) & 0xff).to_bytes(1, 'big'));
        Lcd.write_data((y & 0xff).to_bytes(1, 'big'));
        Lcd.write_data((((y + height - 1) >> 8) & 0xff).to_bytes(1, 'big'));
        Lcd.write_data(((y + height - 1) & 0xff).to_bytes(1, 'big'));        
        
def touch_test():
    """_summary_
    """
    if Touch.read(Position.NORTH_WEST):
        print("Touch north west")
    elif Touch.read(Position.NORTH_EAST):
        print("Touch north east")
    elif Touch.read(Position.SOUTH_WEST):
        print("Touch south west")
    elif Touch.read(Position.SOUTH_EAST):
        print("Touch south east")
        
def touch_irq_test():
    """_summary_
    """
    p4.irq(lambda pin: Touch.handler(), Pin.IRQ_FALLING)
    Touch.attach(Touch.touch_cb)
    Touch.init()
    
def lcd_test():
    """_summary_
    """
    p22.on()
    cs(0)
    utime.sleep(1)
    Lcd.init()
    
    Lcd.set_window(0, 0, 120, 160)
    Lcd.write_cmd(b'\x2c')
    for i in range(120):
        for j in range(160):
            Lcd.write_data(b'\xff')
            Lcd.write_data(b'\xff')
            
    Lcd.set_window(120, 0, 120, 160)
    Lcd.write_cmd(b'\x2c')
    for i in range(120):
        for j in range(160):
            Lcd.write_data(b'\xf8')
            Lcd.write_data(b'\x00')
            
    Lcd.set_window(0, 160, 120, 160)
    Lcd.write_cmd(b'\x2c')
    for i in range(120):
        for j in range(160):
            Lcd.write_data(b'\x07')
            Lcd.write_data(b'\xe0')
            
    Lcd.set_window(120, 160, 120, 160)
    Lcd.write_cmd(b'\x2c')
    for i in range(120):
        for j in range(160):
            Lcd.write_data(b'\x00')
            Lcd.write_data(b'\x1f')
                
def accel_test():
    """_summary_
    """
    if Accel.tilting(Direction.NORTH):
        print('Tilting North !')
    if Accel.tilting(Direction.SOUTH):
        print('Tilting South !')
    if Accel.tilting(Direction.WEST):
        print('Tilting West !')
    if Accel.tilting(Direction.EAST):
        print('Tilting East !')
    if Accel.facing(Direction.FRONT):
        print('Facing front !')
    if Accel.facing(Direction.BACK):
        print('Facing back !')
        
    x = Accel.get_x()
    y = Accel.get_y()
    z = Accel.get_z()
    print('Gravity [x, y ,z] = [{}, {}, {}]'.format(x, y, z))

def christmas():
    """Christmas demo code
    """
    Color = 0x3
    prime1=439
    prime2=17005013
    
    period = .01
    
    # Balles glissantes
    for r in range(20):
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
    for r in range(10):
        Color = (Color * prime1) % prime2
        for i in range(8):
            for j in range(8):
                Matrix.set_led(j,i,Color*(i+1)*(j+11))
        utime.sleep(period)
        Matrix.clear(0)
        utime.sleep(period/10)
    
    # Bleu aléatoire
    period = .05
    for r in range(10):
        Color = (Color * prime1) % prime2
        for i in range(8):
            for j in range(8):
                Matrix.set_led(j,i,Color*(i+1)*(j+11) >> 4)
        utime.sleep(period)

    # Couleurs aleatoire
    period = .05
    for r in range(10):
        Color = (Color * prime1) % prime2
        for i in range(8):
            for j in range(8):
                Matrix.set_led(j,i,Color*(i+1)*(j+11))
        utime.sleep(period)

    # Rouge aléatoire
    period = .05
    for r in range(10):
        Color = (Color * prime1) % prime2
        for i in range(8):
            for j in range(8):
                Matrix.set_led(j,i,Color*(i+1)*(j+11))
        utime.sleep(period)

    # Lignes 
    period = .05
    for r in range(10):
        Color = (Color * prime1) % prime2
        for i in range(8):
            Matrix.set_led(Color%8,i,Color*(i+1)*(j+11))
        utime.sleep(period)
        Matrix.clear(0)
        for i in range(8):
            Matrix.set_led(i,Color%8,Color*(i+1)*(j+11))
        utime.sleep(period)
        Matrix.clear(0)

