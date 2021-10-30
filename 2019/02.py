import re
from advent_of_code import *

def split_code(s):
    return [int(x) for x in s.split(',')]

def run_intcode(values):
    i = 0
    while i < len(values):
        op = values[i]
        if op == 99:
            return values

        v1 = values[values[i + 1]]
        v2 = values[values[i + 2]]
        pos = values[i + 3]

        if op == 1:
            values[pos] = v1 + v2
        else:
            values[pos] = v1 * v2

        i += 4

def run(values, noun, verb):
    values = [*values]
    values[1] = noun
    values[2] = verb
    return run_intcode(values)[0]

run_intcode(
    split_code('1,9,10,3,2,3,11,0,99,30,40,50')
) | eq(split_code('3500,9,10,70,2,3,11,0,99,30,40,50'))

input_str = get_input()
values = split_code(input_str)

run(values, 12, 2) | debug('Star 1')

def run2(values):
    for i in range(100):
        for j in range(100):
            try:
                if run(values, i, j) == 19690720:
                    return (100 * i) + j
            except Exception:
                pass

run2(values) | debug('Star 2')
