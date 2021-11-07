import re
from termcolor import colored
from advent_of_code import *
from int_processor import *

def extract_values(values, ptr, count, mode):
    p = IntProcessor(values, SINGLE_LOOP_MODE)
    p.ptr = ptr
    p.mode = mode

    return p.extract_values(count)

def run(values, inputs):
    p = IntProcessor(values, SINGLE_LOOP_MODE)
    return p.run(inputs=inputs)

extract_values(
    [2, 0, 1], 0, 2, 0
) | eq([1, 2])

extract_values(
    [2, 0, 1], 0, 2, 1
) | eq([2, 2])

extract_values(
    [2, 0, 1], 0, 2, 10
) | eq([1, 0])

extract_values(
    [2, 0, 1], 0, 2, 11
) | eq([2, 0])

example1 = split_comma_ints('3,0,4,0,99')
for i in range(100):
    run(example1, [i]) | eq([i])

input_value = split_comma_ints(get_input())

run(input_value, [1]) | debug('Star 1')

less_than_8 = """
3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99
"""

for i in range(8):
    run(less_than_8, [i])[-1] | eq(999)

run(less_than_8, [8])[-1] | eq(1000)

for i in range(9, 100):
    run(less_than_8, [i])[-1] | eq(1001)

run(input_value, [5]) | debug('Star 2')
