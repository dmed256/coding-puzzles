from advent_of_code import *

input_lines = get_input_lines()

directions = {
    'N': NORTH,
    'S': SOUTH,
    'E': EAST,
    'W': WEST,
}

def run(lines):
    pos = (0, 0)
    direction = EAST
    rotations = {
        'L': COUNTER_CLOCKWISE,
        'R': CLOCKWISE,
    }

    for line in lines:
        op = line[0]
        amount = int(line[1:])
        if op in directions:
            op = directions[op]
            pos = (
                pos[0] + (amount * op[0]),
                pos[1] + (amount * op[1]),
            )
        elif op in ['L', 'R']:
            rotation = rotations[op]
            for i in range(amount // 90):
                direction = rotation[direction]
        else:
            pos = (
                pos[0] + (amount * direction[0]),
                pos[1] + (amount * direction[1]),
            )

    return abs(pos[0]) + abs(pos[1])

example1 = multiline_lines(r"""
F10
N3
F7
R90
F11
""")

run(example1) | eq(25)
run(input_lines) | debug('Star 1') | eq(1838)

def run2(lines):
    pos = (0, 0)
    wpos = (10, 1)

    for line in lines:
        op = line[0]
        amount = int(line[1:])

        if op in directions:
            op = directions[op]
            wpos = (
                wpos[0] + (amount * op[0]),
                wpos[1] + (amount * op[1]),
            )
        elif op in ['L', 'R']:
            (wx, wy) = wpos
            left_rotations = [
                (wx, wy),
                (-wy, wx),
                (-wx, -wy),
                (wy, -wx),
            ]
            left_rotation_count = (amount // 90) % 4
            if op == 'R':
                left_rotation_count = (4 - left_rotation_count) % 4
            wpos = left_rotations[left_rotation_count]
        else:
            pos = (
                pos[0] + (amount * wpos[0]),
                pos[1] + (amount * wpos[1]),
            )

    return abs(pos[0]) + abs(pos[1])

run2(example1) | eq(286)
run2(input_lines) | debug('Star 2') | eq(89936)
