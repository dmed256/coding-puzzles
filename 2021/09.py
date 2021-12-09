from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

def get_basin_size(grid, point):
    q = [point]
    seen = [point]
    while q:
        pos = q.pop(0)
        for n in grid.neighbors(pos):
            if grid[n] != 9 and grid[n] > grid[pos] and n not in seen:
                seen.append(n)
                q.append(n)

    return len(seen)

def run(problem, lines):
    grid = Grid([
        [int(x) for x in line]
        for line in lines
    ])
    low_points = set()
    for (pos, v) in grid:
        if v < min([grid[x] for x in grid.neighbors(pos)]):
            low_points.add(pos)

    if problem == 1:
        return sum([grid[x] + 1 for x in low_points])

    basins = []
    for point in low_points:
        basins.append(get_basin_size(grid, point))

    return mult(sorted(basins)[-3:])

example1 = multiline_lines(r"""
2199943210
3987894921
9856789892
8767896789
9899965678
""")

run(1, example1) | eq(15)

run(1, input_lines) | debug('Star 1') | eq(562)

run(2, example1) | eq(1134)

run(2, input_lines) | debug('Star 2') | eq(1076922)
