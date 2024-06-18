from hl3 import *
import time

matrix.clear(0)

matrix.set_led(5, 5, color.GREEN)
print(matrix.get_led(5,5))

for i in range(8):
    matrix.set_line(i, color.RED)
    time.sleep(0.1)
    matrix.set_line(i, 0)

for i in range(8):
    matrix.set_column(i, color.RED)
    time.sleep(0.1)
    matrix.set_column(i, 0)
    
for i in range(8):
    for j in range(8):
        matrix.set_led(j, i, color.RED)
        time.sleep(0.1)
        matrix.set_led(j, i, 0)
