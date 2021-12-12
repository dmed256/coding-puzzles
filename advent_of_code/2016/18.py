from repo_utils import *

input_lines = get_input_lines()

def run(problem, lines, rows):
    grid = [lines[0]]
    cols = len(grid[0])

    for r in range(1, rows):
        prev_row = grid[r - 1]
        next_row = ''
        for c in range(cols):
            t1, t2, t3 = [
                prev_row[c2] == '^' if 0 <= c2 < cols else False
                for c2 in [c - 1, c, c + 1]
            ]
            if ((t1 and t2 and not t3) or
                (t2 and t3 and not t1) or
                (t1 and not t2 and not t3) or
                (t3 and not t1 and not t2)):
                next_row += '^'
            else:
                next_row += '.'

        grid.append(next_row)

    return Grid(grid).count('.')

example1 = multiline_lines(r"""
.^^.^.^^^^
""")

run(1, example1, 10) | eq(38)

run(1, input_lines, 40) | submit(1)

# run(2, example1) | eq()

# run(2, input_lines) | submit(2)
