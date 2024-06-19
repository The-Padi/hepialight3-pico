from hl3 import *

#uart_north = Uart(Direction.NORTH)
#uart_south = Uart(Direction.SOUTH)
uart_east = Uart(Direction.EAST, 9600)
#uart_west = Uart(Direction.WEST)


while True:
    #uart_east.sendline("Pipo")
    received_data = uart_east.receiveline()
    #received_data = uart_north.receiveline()
    print(f"Data received: {received_data}")
    #utime.sleep(0.1)
