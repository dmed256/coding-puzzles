from advent_of_code import *

def find_pos(value, problem):
    pos = (0, 0)
    radius = 0
    idx = 1

    if idx > value:
        return idx, pos

    grid = { pos: idx }

    if problem == 1:
        def increment_index(pos):
            return idx + 1
    else:
        def increment_index(pos):
            new_index = 0
            for direction in DIAG_DIRECTIONS:
                n = apply_direction(pos, direction)
                if n in grid:
                    new_index += grid[n]
            return new_index

    while True:
        radius += 1

        for direction in [UP, LEFT, DOWN, RIGHT]:
            for i in range(2*radius):
                direction_i = (
                    RIGHT
                    if i == 0 and direction == UP else
                    direction
                )
                pos = apply_direction(pos, direction_i)

                idx = increment_index(pos)
                grid[pos] = idx
                if idx > value:
                    return idx, pos

def run(value, problem):
    if problem == 1:
        idx, pos = find_pos(value - 1, problem)
        return pos_distance(pos)

    idx, pos = find_pos(value - 1, problem)
    return idx

run(1, 1) | eq(0)
run(12, 1) | eq(3)
run(23, 1) | eq(2)
run(1024, 1) | eq(31)
run(312051, 1) | debug('Star 1') | eq(430)

run(1, 2) | eq(1)
run(5, 2) | eq(5)
run(10, 2) | eq(10)
run(760, 2) | eq(806)
run(806, 2) | eq(806)
run(312051, 2) | debug('Star 2') | eq(312453)
