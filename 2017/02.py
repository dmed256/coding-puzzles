import re
from advent_of_code import *

input_lines = get_input_lines()

def get_grid(lines):
    return [
        [int(v) for v in re.split(r'\s+', line)]
        for line in lines
    ]

def run(lines):
    grid = get_grid(lines)
    return sum(
        max(row) - min(row)
        for row in grid
    )

example1 = multiline_lines(r"""
5 1 9 5
7 5 3
2 4 6 8
""")

run(example1) | eq(18)

run(input_lines) | debug('Star 1') | eq(37923)

def run2(lines):
    grid = get_grid(lines)

    def get_divisor_value(row):
        for i, v1 in enumerate(row):
            for v2 in row[i+1:]:
                if v1 % v2 == 0:
                    return v1 // v2
                if v2 % v1 == 0:
                    return v2 // v1

    return sum(
        get_divisor_value(row)
        for row in grid
    )

example1 = multiline_lines(r"""
5 9 2 8
9 4 7 3
3 8 6 5
""")

run2(example1) | eq(9)

run2(input_lines) | debug('Star 2') | eq(263)
