from repo_utils import *

input_lines = get_input_lines()

def advance(grid):
    moved = False
    moves = []
    for y in range(grid.height):
        for x in range(grid.width):
            x2 = (x + 1) % grid.width
            if grid[(x, y)] != '>':
                continue

            if grid[(x2, y)] == '.':
                moves.append([(x, y), (x2, y)])

    for pos1, pos2 in moves:
        moved = True
        grid[pos2] = grid[pos1]
        grid[pos1] = '.'

    moves = []
    for x in range(grid.width):
        for y in range(grid.height):
            y2 = (y + 1) % grid.height
            if grid[(x, y)] != 'v':
                continue

            if grid[(x, y2)] == '.':
                moves.append([(x, y), (x, y2)])

    for pos1, pos2 in moves:
        moved = True
        grid[pos2] = grid[pos1]
        grid[pos1] = '.'

    return grid, moved


def run(problem, lines):
    grid = Grid(lines)

    for step in range(1, 1000000000):
        grid, moved = advance(grid)
        if not moved:
            return step

example1 = multiline_lines(r"""
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
""")

run(1, example1) | eq(58)

run(1, input_lines) | debug('Star 1') | eq(384)
