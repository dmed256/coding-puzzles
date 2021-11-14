from advent_of_code import *

def run(value, problem):
    if value == 1:
        return 0

    if problem == 1:
        def increment_index(pos, idx):
            return idx + 1
    else:
        def increment_index(pos, idx):
            return idx + 1

    pos = (0, 0)
    radius = 0
    idx = 1

    grid = { pos: idx }
    while grid[pos] < value:
        radius += 1

        for direction in [UP, LEFT, DOWN, RIGHT]:
            for i in range(radius + 1):
                if i == 0 and direction == UP:
                    pos = apply_direction(pos, RIGHT)
                else:
                    pos = apply_direction(pos, direction)

                idx = increment_index(pos, idx)
                print(f'{pos}: {idx}')
                grid[pos] = idx
                if idx >= value:
                    print(pos)
                    return pos_distance(pos)

# run(1, 1) | eq(0)
# run(12, 1) | eq(3)
run(23, 1) | eq(2)
# run(1024, 1) | eq(31)
# run(312051, 1) | debug('Star 1') | eq(430)

# run2(example1) | eq()

# run2(input_lines) | debug('Star 2')
