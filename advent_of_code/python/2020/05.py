import math
from repo_utils import *

input_value = get_input()
input_lines = get_input_lines()

def get_seat(line):
    x = [0, 127]
    y = [0, 7]
    for c in line:
        x_mid = sum(x) / 2
        y_mid = sum(y) / 2
        if c == 'F':
            x[1] = math.floor(x_mid)
        elif c == 'B':
            x[0] = math.ceil(x_mid)
        elif c == 'L':
            y[1] = math.floor(y_mid)
        else:
            y[0] = math.ceil(y_mid)

    return (x[0] * 8) + y[0]

def run(lines):
    return max([
        get_seat(line)
        for line in lines
    ])

run(['FBFBBFFRLR']) | eq(357)
run(['BFFFBBFRRR']) | eq(567)
run(['FFFBBBFRRR']) | eq(119)
run(['BBFFBBFRLL']) | eq(820)

run(input_lines) | debug('Star 1') | eq(896)

def run2(lines):
    seats = sorted([
        get_seat(line)
        for line in lines
    ])
    count = (seats[0] + seats[-1]) * (len(seats) + 1) // 2
    return count - sum(seats)

run2(input_lines) | debug('Star 2') | eq(659)
