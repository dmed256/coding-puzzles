from repo_utils import *

def make_grid(cols, rows):
    return Grid([
        [0 for col in range(cols)]
        for row in range(rows)
    ])

def run(problem, grid_number):
    grid = make_grid(300, 300)
    for pos, _ in grid:
        x, y = pos

        rack_id = x + 10
        power_level = rack_id * y
        power_level += grid_number
        power_level *= rack_id

        power_level = (power_level % 1000) // 100
        power_level -= 5

        grid[pos] = power_level

    original_grid = grid.copy()


    max_info = None
    max_power = -1e20
    for square_size in range(2, 300):
        small_grid = make_grid(grid.width - 1, 300)

        for pos, _ in small_grid:
            x, y = pos
            next_pos = (x + square_size - 1, y)

            small_grid[pos] = (
                grid[pos]
                + original_grid[next_pos]
            )

        square_info = None
        square_max_power = -1e20
        for pos, _ in small_grid:
            x, y = pos
            if 300 <= y + square_size:
                continue

            value = sum(
                small_grid[(x, y)]
                for y in range(y, y + square_size)
            )
            if square_max_power < value:
                square_info = (*pos, square_size)
                square_max_power = value

        if problem == 1 and square_size == 3:
            x, y, _ = square_info
            return f'{x},{y}'

        if max_power <= square_max_power:
            max_power = square_max_power
            max_info = square_info
        else:
            break

        grid = small_grid

    x, y, size = max_info
    return f'{x},{y},{size}'


run(1, 18) | eq('33,45')
run(1, 42) | eq('21,61')

run(1, 5235) | debug('Star 1') | eq('33,54')

run(2, 18) | eq('90,269,16')
run(2, 42) | eq('232,251,12')

run(2, 5235) | debug('Star 2') | eq('232,289,8')
