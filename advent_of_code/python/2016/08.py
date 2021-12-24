from repo_utils import *

input_value = get_input()
input_lines = get_input_lines()

def run(problem, lines, width, height):
    grid = Grid([
        [0 for c in range(width)]
        for r in range(height)
    ])

    for line in lines:
        ins, *other = line.split()
        next_grid = grid.copy()

        if ins == 'rect':
            cols, rows = other[0].split('x')
            cols = int(cols)
            rows = int(rows)

            for y in range(rows):
                for x in range(cols):
                    next_grid[(x, y)] = 1
        elif ins == 'rotate':
            rc, pivot, by, shift = other

            pivot = int(pivot.split('=')[1])
            shift = int(shift)

            if rc == 'row':
                y = pivot
                for x in range(next_grid.width):
                    x2 = (x + shift) % next_grid.width
                    next_grid[(x2, y)] = grid[(x, y)]
            else:
                x = pivot
                for y in range(next_grid.height):
                    y2 = (y + shift) % next_grid.height
                    next_grid[(x, y2)] = grid[(x, y)]

        grid = next_grid

    lights = grid.count(1)

    if problem == 2:
        grid.replace(0, ' ')
        grid.replace(1, '#')
        grid.print(use_padding=False)

    return lights

example1 = multiline_lines(r"""
rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1
""")

run(1, example1, 7, 3) | eq(6)

run(1, input_lines, 50, 6) | debug('Star 1') | eq(110)

run(2, input_lines, 50, 6) | debug('Star 2') | eq(110)
