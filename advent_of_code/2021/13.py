from repo_utils import *

input_lines = get_input_lines()

def run(problem, lines):
    coords = set()
    folds = []
    for line in lines:
        if not line:
            continue
        if line.startswith('fold'):
            axis, value = line.split()[-1].split('=')
            folds.append((axis, int(value)))
        else:
            x, y = line.split(',')
            coords.add((int(x), int(y)))

    def print_coord(coords):
        max_x = max(x for x, y in coords)
        min_x = min(x for x, y in coords)
        max_y = max(y for x, y in coords)
        min_y = min(y for x, y in coords)
        grid = Grid([
            ['.' for x in range(min_x, max_x + 1)]
            for y in range(min_y, max_y + 1)
        ])
        for x, y in coords:
            grid[(x, y)] = '#'
        grid.print()

    for axis, value in folds:
        new_coords = set()
        for x, y in coords:
            if axis == 'y':
                if y > value:
                    diff = y - value
                    y2 = value - diff
                    new_coords.add((x, y2))
                else:
                    new_coords.add((x, y))
            else:
                if x > value:
                    diff = x - value
                    x2 = value - diff
                    new_coords.add((x2, y))
                else:
                    new_coords.add((x, y))
        coords = new_coords
        if problem == 1:
            break

    if problem == 2:
        print_coord(coords)
        return

    return len(coords)

example1 = multiline_lines(r"""
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
""")

run(1, example1) | eq(17)

run(1, input_lines) | debug('Star 1') | eq(618)

run(2, input_lines) | debug('Star 2')
