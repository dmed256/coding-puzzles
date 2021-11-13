import itertools
from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

def run(lines, value):
    values = [int(v) for v in lines]
    return sum((
        1
        for i in range(len(values))
        for combination in itertools.combinations(values, i)
        if sum(combination) == value
    ))

example1 = multiline_lines(r"""
20
15
10
5
5
""")

run(example1, 25) | eq(4)

run(input_lines, 150) | debug('Star 1') | eq(4372)

def run2(lines, value):
    values = [int(v) for v in lines]
    for i in range(len(values)):
        combinations_found = 0
        for combination in itertools.combinations(values, i):
            combinations_found += sum(combination) == value
        if combinations_found:
            break

    return combinations_found

run2(example1, 25) | eq(3)
run2(input_lines, 150) | debug('Star 2') | eq(4)
