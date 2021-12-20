from repo_utils import *

input_lines = get_input_lines()

EMPTY = 0
WALL = 1
WATER = 2
WATERFALL = 3

DROP = 0
SPREAD = 1


def get_spread_surface(grid, pos):
    spaces = []
    walls = []
    drops = []

    # Can't spread when there is no surface
    if not grid.apply_direction(pos, GRID_DOWN):
        return spaces, walls, drops

    spaces.append(pos)

    for direction in [GRID_LEFT, GRID_RIGHT]:
        npos = pos
        while True:
            npos = grid.apply_direction(npos, direction)
            if not npos:
                break

            # Stop spreading water
            if grid[npos] == WALL:
                walls.append(npos)
                break

            # Can only spread on top of WATER and WALL surfaces
            down_pos = grid.apply_direction(npos, GRID_DOWN)
            down = grid[down_pos]

            if down in [WATER, WALL]:
                spaces.append(npos)
                continue

            # There is an empty space, water needs to flow down
            if down == EMPTY:
                drops.append(npos)

            break

    return spaces, walls, drops

def can_water_rise(grid, pos):
    _, walls, _ = get_spread_surface(grid, pos)
    return len(walls) == 2

def drop_water(grid, pos):
    while pos:
        # Nothing more to do
        if grid[pos] in [WATER, WATERFALL]:
            return []

        grid[pos] = WATERFALL

        prev_pos = pos
        pos = grid.apply_direction(pos, GRID_DOWN)

        if not pos:
            break

        v = grid[pos]
        if v == EMPTY:
            continue

        if v == WALL or can_water_rise(grid, pos):
            return [(prev_pos, SPREAD)]

        break

    return []


def spread_water(grid, source_pos):
    effects = []
    spaces, walls, drops = get_spread_surface(grid, source_pos)

    for pos in spaces:
        grid[pos] = WATERFALL if drops else WATER

    effects += [
        (pos, DROP)
        for pos in drops
    ]

    if len(walls) == 2:
        up_pos = grid.apply_direction(source_pos, GRID_UP)
        effects += [(up_pos, SPREAD)]

    return effects


def build_grid(lines):
    wall_points = set()
    for line in lines:
        left, right = line.split(', ')

        axis1, value1 = left.split('=')
        value1 = int(value1)

        axis2, values2 = right.split('=')
        min_value2, max_value2 = [int(x) for x in values2.split('..')]

        for value2 in range(min_value2, max_value2 + 1):
            if axis1 == 'x':
                wall_points.add((value1, value2))
            else:
                wall_points.add((value2, value1))

    # We're going to pad the x values in case the water goes
    # out of bounds by 1 by each side
    min_x = min(x for x, y in wall_points) - 1
    min_y = min(y for x, y in wall_points)
    max_x = max(x for x, y in wall_points) - min_x + 1
    max_y = max(y for x, y in wall_points) - min_y

    wall_points = [
        (x - min_x, y - min_y)
        for x, y in wall_points
    ]
    corner_points = [
        (0, 0),
        (max_x, 0),
        (0, max_y),
        (max_x, max_y),
    ]

    grid = Grid.from_points(
        wall_points + corner_points,
        set_value=WALL,
        unset_value=EMPTY,
    )
    for point in corner_points:
        grid[point] = EMPTY

    start_pos = (500 - min_x, 0)

    return grid, start_pos


def print_grid(grid, pos=None, color=True):
    if pos:
        x, y = pos or (0, 0)

        min_x = max(0, x - 100)
        max_x = min(grid.width, min_x + 200)

        min_y = max(0, y - 25)
        max_y = min(grid.height, min_y + 50)

        grid = Grid([
            [grid[(x, y)] for x in range(min_x, max_x)]
            for y in range(min_y, max_y)
        ])

        pos = (x - min_x, y - min_y)
    else:
        grid = grid.copy()

    empty_char = ' '
    wall_char = '#'
    water_char = '~'
    waterfall_char = '|'
    if color:
        wall_char = yellow(wall_char)
        water_char = blue(water_char)
        waterfall_char = blue(waterfall_char)

    if pos:
        grid[pos] = red('X')

    grid.replace(EMPTY, empty_char)
    grid.replace(WALL, wall_char)
    grid.replace(WATER, water_char)
    grid.replace(WATERFALL, waterfall_char)

    grid.print()
    input()


def run(problem, lines):
    grid, start_pos = build_grid(lines)

    queue = deque([(start_pos, DROP)])
    while queue:
        pos, movement = queue.pop()

        if movement == DROP:
            queue += drop_water(grid, pos)
        elif movement == SPREAD:
            queue += spread_water(grid, pos)

        # print_grid(grid, pos=pos)

    # print_grid(grid)
    counter = grid.get_counter()

    if problem == 1:
        return counter[WATER] + counter[WATERFALL]
    else:
        return counter[WATER]


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

run(1, input_lines) | debug('Star 1') | eq(27736)

run(2, example1) | eq(29)

run(2, input_lines) | debug('Star 2') | eq(22474)
