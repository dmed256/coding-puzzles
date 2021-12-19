from repo_utils import *

input_lines = get_input_lines()

OPEN = '.'
TREE = '|'
LUMBERYARD = '#'

def run(problem, lines):
    minutes = 10 if problem == 1 else 1000000000

    def get_grid_key(grid):
        return ''.join(
            c
            for row in grid.rows
            for c in row
        )

    def get_resource_value(grid_key):
        resources = Counter(grid_key)
        return resources[TREE] * resources[LUMBERYARD]

    grid = Grid(lines)
    grid_key = get_grid_key(grid)

    grid_indices = {grid_key: 0}
    grid_resource_values = [get_resource_value(grid_key)]

    for elapsed_minute in range(1, minutes + 1):
        next_grid = grid.copy()
        for pos, v in grid:
            neighbors = Counter(
                grid[npos]
                for npos in grid.neighbors(pos, DIAG_DIRECTIONS)
            )
            if v == OPEN and neighbors[TREE] >= 3:
                next_grid[pos] = TREE
            elif v == TREE and neighbors[LUMBERYARD] >= 3:
                next_grid[pos] = LUMBERYARD
            elif v == LUMBERYARD and (not neighbors[LUMBERYARD] or not neighbors[TREE]):
                next_grid[pos] = OPEN

        grid = next_grid
        grid_key = get_grid_key(grid)

        if grid_key in grid_indices:
            break

        grid_indices[grid_key] = elapsed_minute
        grid_resource_values.append(
            get_resource_value(grid_key)
        )

    if elapsed_minute == minutes:
        grid_idx = minutes
    else:
        cycle_start = grid_indices[grid_key]
        cycle_length = len(grid_indices) - cycle_start

        grid_idx = cycle_start + ((minutes - cycle_start) % cycle_length)

    return grid_resource_values[grid_idx]

example1 = multiline_lines(r"""
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
""")

run(1, example1) | eq(1147)

run(1, input_lines) | debug('Star 1') | eq(560091)

run(2, input_lines) | debug('Star 2') | eq(202301)
