from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

def run(lines, slopes):
    tree_positions = {
        (x, y)
        for y, line in enumerate(lines)
        for x, c in enumerate(line)
        if c == '#'
    }
    height = len(lines)
    width = len(lines[0])

    value = 1
    for (dx, dy) in slopes:
        trees = 0
        x = 0
        for y in range(0, height, dy):
            if (x, y) in tree_positions:
                trees += 1
            x = (x + dx) % width
        value *= trees
    return value


example1 = multiline_lines(r"""
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
""")

slopes = [(3, 1)]
run(example1, slopes) | eq(7)

run(input_lines, slopes) | debug('Star 1') | eq(220)

slopes = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]
run(example1, slopes) | eq(336)

run(input_lines, slopes) | debug('Star 2') | eq(2138320800)
