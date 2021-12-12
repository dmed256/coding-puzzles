from repo_utils import *

input_value = get_input()
input_lines = get_input_lines()

def run(lines, steps, problem):
    grid = Grid(lines)
    neighbors = {
        pos: grid.neighbors(pos, DIAG_DIRECTIONS)
        for pos, v in grid
    }

    def set_corners(grid):
        if problem == 1:
            return
        grid[(0, 0)] = '#'
        grid[(grid.width - 1, 0)] = '#'
        grid[(0, grid.height - 1)] = '#'
        grid[(grid.width - 1, grid.height - 1)] = '#'

    for i in range(steps):
        set_corners(grid)
        next_grid = grid.copy()
        for pos, v in grid:
            lights = len([
                1
                for n in neighbors[pos]
                if grid[n] == '#'
            ])
            if v == '#':
                is_on = 2 <= lights <= 3
            else:
                is_on = lights == 3

            next_grid[pos] = '#' if is_on else '.'
        grid = next_grid

    set_corners(grid)
    return len([
        1
        for pos, v in grid
        if v == '#'
    ])

example1 = multiline_lines(r"""
.#.#.#
...##.
#....#
..#...
#.#..#
####..
""")

run(example1, 4, 1) | eq(4)
run(input_lines, 100, 1) | debug('Star 1') | eq(814)

run(example1, 5, 2) | eq(17)
run(input_lines, 100, 2) | debug('Star 2') | eq(924)
