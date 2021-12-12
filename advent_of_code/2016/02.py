from repo_utils import *

input_value = get_input()
input_lines = get_input_lines()

def run(problem, lines):
    if problem == 1:
        grid = Grid([
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
        ])
        pos = (1, 1)
    else:
        grid = Grid([
            ['', '', '1', '', ''],
            ['', '2', '3', '4', ''],
            ['5', '6', '7', '8', '9'],
            ['', 'A', 'B', 'C', ''],
            ['', '', 'D', '', ''],
        ])
        pos = (0, 3)

    value = ''
    for line in lines:
        for c in line:
            direction = {
                'L': GRID_LEFT,
                'R': GRID_RIGHT,
                'U': GRID_UP,
                'D': GRID_DOWN,
            }[c]
            next_pos = grid.apply_direction(pos, direction)
            if next_pos is not None and grid[next_pos]:
                pos = next_pos

        value += grid[pos]

    return value

run(1, input_lines) | debug('Star 1') | eq('61529')

run(2, input_lines) | debug('Star 2') | eq('C2C28')
