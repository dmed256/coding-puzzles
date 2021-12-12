from repo_utils import *

input_value = get_input()
input_lines = get_input_lines()

def run(problem, lines):
    values = lines[0].split(', ')

    pos = (0, 0)
    direction = UP

    visited = set(pos)
    for value in values:
        turn = value[0]
        dist = int(value[1:])

        if turn == 'R':
            direction = CLOCKWISE[direction]
        else:
            direction = COUNTER_CLOCKWISE[direction]

        for _ in range(dist):
            pos = apply_direction(pos, direction)
            if problem == 2 and pos in visited:
                return abs(pos[0]) + abs(pos[1])
            visited.add(pos)

    return abs(pos[0]) + abs(pos[1])

run(1, input_lines) | debug('Star 1') | eq(241)

run(2, input_lines) | debug('Star 2') | eq(116)
