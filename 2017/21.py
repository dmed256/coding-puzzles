from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

def split_image(img):
    return [
        [c for c in row]
        for row in img.split('/')
    ]

def join_image(img):
    return '/'.join([
        ''.join(row)
        for row in img
    ])

def get_arrangements(img):
    grid = split_image(img)
    arrangements = []
    for _ in range(2):
        for rotation in range(4):
            arrangements.append(grid)
            grid = [
                [row[c] for row in reversed(grid)]
                for c in range(len(grid))
            ]
        grid = grid[::-1]

    return [
        join_image(grid)
        for grid in arrangements
    ]

def get_subgrid(grid, r, c, size):
    return [
        [
            grid[ri][ci]
            for ri in range(r, r + size)
        ]
        for ci in range(c, c + size)
    ]

def split(grid, transforms, size):
    width = len(grid)
    expanded_grid = []
    for r in range(0, width, size):
        big_row = None
        for c in range(0, width, size):
            subgrid = get_subgrid(grid, r, c, size)
            subgrid = transforms[join_image(subgrid)]
            subgrid = split_image(subgrid)

            if big_row is None:
                big_row = [[] for i in range(len(subgrid))]
            for i, row in enumerate(subgrid):
                big_row[i] += row

        for row in big_row:
            expanded_grid.append(row)

    return expanded_grid

def run(lines, iterations):
    transforms = {}
    for line in lines:
        left, right = line.split(' => ')
        for arrangement in get_arrangements(left):
            transforms[arrangement] = right

    grid = [
        [c for c in row]
        for row in '.#./..#/###'.split('/')
    ]

    for i in range(iterations):
        if len(grid) % 2 == 0:
            grid = split(grid, transforms, 2)
        else:
            grid = split(grid, transforms, 3)

    return len([
        1
        for row in grid
        for c in row
        if c == '#'
    ])

example1 = multiline_lines(r"""
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
""")

run(example1, 2) | eq(12)

run(input_lines, 5) | debug('Star 1') | eq(208)

run(input_lines, 18) | debug('Star 2') | eq(2480380)
