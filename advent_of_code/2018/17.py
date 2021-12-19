from repo_utils import *

input_lines = get_input_lines()

DOWN = 0
STILL = 1
OVERFLOWING = 2

def run(problem, lines):
    points = set()
    for line in lines:
        left, right = line.split(', ')

        axis1, value1 = left.split('=')
        value1 = int(value1)

        axis2, values2 = right.split('=')
        min_value2, max_value2 = [int(x) for x in values2.split('..')]

        for value2 in range(min_value2, max_value2 + 1):
            if axis1 == 'x':
                points.add((value1, value2))
            else:
                points.add((value2, value1))

    # We're going to pad the x values in case the water goes
    # out of bounds by 1 by each side
    min_x = min(x for x, y in points) - 1
    min_y = min(y for x, y in points)
    max_x = max(x for x, y in points) - min_x + 1
    max_y = max(y for x, y in points) - min_y

    points = [
        (x - min_x, y - min_y)
        for x, y in points
    ]
    corner_points = [
        (0, 0),
        (max_x, 0),
        (0, max_y),
        (max_x, max_y),
    ]

    grid = Grid.from_points(
        points + corner_points
    )
    for point in corner_points:
        grid[point] = '.'

    grid.print()

    return None

example1 = multiline_lines(r"""
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
""")

run(1, example1) | eq(57)

run(1, input_lines) | submit(1)

# run(2, example1) | eq()

# run(2, input_lines) | submit(2)
