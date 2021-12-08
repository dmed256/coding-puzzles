from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

def run(problem, lines, iterations):
    def parse(s):
        return s.split('/')

    def stringify(img):
        return '/'.join(img)

    maps = {}
    for line in lines:
        [left, right] = line.split(' => ')

        def rotate(img):
            img = parse(img)
            size = len(img)
            return stringify([
                ''.join(row[i] for row in reversed(img))
                for i in range(size)
            ])

        for flip_ in range(2):
            for rotation in range(4):
                maps[left] = right
                left = rotate(left)
            left = left[::-1]

    def split(grid):
        grid = [
            [parse(img) for img in row]
            for row in grid
        ]
        next_grid = []
        for row in grid:
            next_row1 = []
            next_row2 = []
            for img in row:
                split_img = [
                    img_row[2*r:2*r+2]
                    for img_row in img
                    for r in range(2)
                ]
                next_row1 += [
                    stringify([split_img[0], split_img[2]]),
                    stringify([split_img[1], split_img[3]]),
                ]
                next_row2 += [
                    stringify([split_img[4], split_img[6]]),
                    stringify([split_img[5], split_img[7]]),
                ]
            next_grid.append(next_row1)
            next_grid.append(next_row2)

        return next_grid


    grid = [['.#./..#/###']]
    size = 3
    for i in range(iterations):
        grid = [
            [maps[img] for img in row]
            for row in grid
        ]
        if size == 3:
            grid = split(grid)
            size = 2
        else:
            size = 3

    count = 0
    for row in grid:
        for img in row:
            count += len([c for c in img if c == '#'])
    return count

example1 = multiline_lines(r"""
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
""")

run(1, example1, 2) | eq(12)

# run(1, input_lines, 5) | debug('Star 1') | clipboard()

# run(2, example1) | eq()

# run(2, input_lines) | debug('Star 2') | clipboard()
