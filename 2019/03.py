import re
from advent_of_code import *

def traverse_wire(wire):
    x = 0
    y = 0
    total_distance = 0

    vlines = []
    hlines = []
    for word in wire:
        op = word[0]
        distance = int(word[1:])

        x2 = x
        y2 = y
        if op == 'R':
            x2 = x + distance
            hlines.append([y, x, x2, op, total_distance])
        elif op == 'L':
            x2 = x - distance
            hlines.append([y, x2, x, op, total_distance])
        elif op == 'U':
            y2 = y2 + distance
            vlines.append([x, y, y2, op, total_distance])
        elif op == 'D':
            y2 = y2 - distance
            vlines.append([x, y2, y, op, total_distance])

        x = x2
        y = y2
        total_distance += distance

    return hlines, vlines

def get_steps(x_info, y_info):
    [x_op, x_distance, x1, x, x2] = x_info
    [y_op, y_distance, y1, y, y2] = y_info

    if x_op == 'L':
        x_distance = x_distance + abs(x2 - x)
    else:
        x_distance = x_distance + abs(x - x1)

    if y_op == 'D':
        y_distance = y_distance + abs(y2 - y)
    else:
        y_distance = y_distance + abs(y - y1)

    return x_distance + y_distance


def find_line_intersections(hlines, vlines):
    hlines.sort()
    vlines.sort()

    return [
        (x, y, get_steps([x_op, x_distance, x1, x, x2], [y_op, y_distance, y1, y, y2]))
        for [x, y1, y2, y_op, x_distance] in vlines
        for [y, x1, x2, x_op, y_distance] in hlines
        if y1 <= y <= y2 and x1 <= x <= x2 and (x, y) != (0, 0)
    ]

def find_intersections(lines):
    wire1 = lines[0].split(',')
    wire2 = lines[1].split(',')

    hlines1, vlines1 = traverse_wire(wire1)
    hlines2, vlines2 = traverse_wire(wire2)

    return [
        *find_line_intersections(hlines1, vlines2),
        *find_line_intersections(hlines2, vlines1),
    ]

def run(lines):
    return min(
        abs(x) + abs(y)
        for (x, y, d) in find_intersections(lines)
    )

example1 = [
    'R8,U5,L5,D3',
    'U7,R6,D4,L4',
]
example2 = [
    'R75,D30,R83,U83,L12,D49,R71,U7,L72',
    'U62,R66,U55,R34,D71,R55,D58,R83',
]
example3 = [
    'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
    'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7',
]

run(example1) | eq(6)
run(example2) | eq(159)
run(example3) | eq(135)

input_lines = get_input_lines()

run(input_lines) | debug('Star 1')

def run2(lines):
    return min(
        d
        for (x, y, d) in find_intersections(lines)
    )

run2(example1) | eq(30)
run2(example2) | eq(610)
run2(example3) | eq(410)

run2(input_lines) | debug('Star 2')
