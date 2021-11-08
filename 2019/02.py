import re
from advent_of_code import *
from int_processor import *

input_value = get_input()

def run(noun, verb):
    p = IntProcessor(input_value)
    p.original_values[1] = noun
    p.original_values[2] = verb

    p.run()
    return p.values[0]

run(12, 2) | debug('Star 1') | eq(7210630)

def run2():
    for i in range(100):
        for j in range(100):
            if run(i, j) == 19690720:
                return (100 * i) + j

run2() | debug('Star 2') | eq(3892)
