from repo_utils import *

input_lines = get_input_lines()

trap_values = {
    (1 << 0),
    (1 << 0) + (1 << 1),
    (1 << 1) + (1 << 2),
    (1 << 2),
}

def run(problem, lines, rows):
    grid = [lines[0]]
    cols = len(grid[0])

    prev_row = [1 if c == '^' else 0 for c in lines[0]]
    trap_tiles = sum(prev_row)

    for r in range(1, rows):
        next_row = []
        for c in range(cols):
            t0, t1, t2 = [
                prev_row[c2] if 0 <= c2 < cols else 0
                for c2 in [c - 1, c, c + 1]
            ]
            checksum = (t0 << 0) + (t1 << 1) + (t2 << 2)
            next_row.append(1 if checksum in trap_values else 0)

        prev_row = next_row
        trap_tiles += sum(prev_row)

    return (rows * cols) - trap_tiles

example1 = multiline_lines(r"""
.^^.^.^^^^
""")

run(1, example1, 10) | eq(38)

run(1, input_lines, 40) | debug('Star 1') | eq(1956)

run(2, input_lines, 400000) | debug('Star 2') | eq(19995121)
