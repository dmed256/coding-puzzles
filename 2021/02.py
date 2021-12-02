from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

def parse_lines(lines):
    return [
        [entries[0], int(entries[1])]
        for line in lines
        if (entries := line.split(' '))
    ]


def run(lines):
    depth = 0
    horizontal = 0
    for [instruction, value] in parse_lines(lines):
        if instruction == 'down':
            depth += value
        if instruction == 'up':
            depth -= value
        if instruction == 'forward':
            horizontal += value
    return horizontal * depth

example1 = multiline_lines(r"""
forward 5
down 5
forward 8
up 3
down 8
forward 2
""")

run(example1) | eq(150)

run(input_lines) | debug('Star 1') | eq(1855814)

def run2(lines):
    aim = 0
    depth = 0
    horizontal = 0
    for [instruction, value] in parse_lines(lines):
        if instruction == 'down':
            aim += value
        if instruction == 'up':
            aim -= value
        if instruction == 'forward':
            horizontal += value
            depth += aim * value
    return horizontal * depth

run2(example1) | eq(900)

run2(input_lines) | debug('Star 2') | eq(1845455714)
