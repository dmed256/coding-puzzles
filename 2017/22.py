from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

CLEAN = 0
WEAKENED = 1
INFECTED = 2
FLAGGED = 3

def run(problem, lines):
    grid = Grid(lines)

    node_statuses = {}
    for (pos, v) in grid:
        if v == '#':
            node_statuses[pos] = INFECTED

    pos = grid.center()
    direction = GRID_UP

    infection_count = 0
    if problem == 1:
        for _ in range(10000):
            status = node_statuses.get(pos, CLEAN)

            if status == CLEAN:
                direction = GRID_COUNTER_CLOCKWISE[direction]
                node_statuses[pos] = INFECTED
                infection_count += 1
            else:
                direction = GRID_CLOCKWISE[direction]
                del node_statuses[pos]

            pos = apply_direction(pos, direction)

        return infection_count

    for _ in range(10000000):
        status = node_statuses.get(pos, CLEAN)

        if status == CLEAN:
            direction = GRID_COUNTER_CLOCKWISE[direction]
        elif status == INFECTED:
            direction = GRID_CLOCKWISE[direction]
        elif status == FLAGGED:
            direction = (-direction[0], -direction[1])

        status = (status + 1) % 4
        if status == CLEAN:
            del node_statuses[pos]
        else:
            if status == INFECTED:
                infection_count += 1
            node_statuses[pos] = status

        pos = apply_direction(pos, direction)

    return infection_count

example1 = multiline_lines(r"""
..#
#..
...
""")

run(1, example1) | eq(5587)

run(1, input_lines) | debug('Star 1') | eq(5552)

run(2, example1) | eq(2511944)

run(2, input_lines) | debug('Star 2') | eq(2511527)
