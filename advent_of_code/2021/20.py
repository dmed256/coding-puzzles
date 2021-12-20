from repo_utils import *

from itertools import product
input_lines = get_input_lines()

DIRECTIONS = [
    (-1, -1),
    (0, -1),
    (1, -1),
    (-1, 0),
    (0, 0),
    (1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
]

def neighbors(pos):
    return [
        apply_direction(pos, direction)
        for direction in DIRECTIONS
    ]

def apply_algo(lights, algo, iteration):
    # Flip what on/off means
    if algo[0] == 1 and algo[-1] == 0:
        on_value = (iteration % 2 == 0)
        on_value2 = not on_value
    else:
        on_value = 1
        on_value2 = 1

    positions = {
        apply_direction(pos, direction)
        for pos in lights
        for direction in DIRECTIONS
    }

    lights2 = set()
    for pos in positions:
        value = ''.join([
            '1' if (npos in lights) == on_value else '0'
            for npos in neighbors(pos)
        ])
        if algo[int(value, 2)] == on_value2:
            lights2.add(pos)

    return lights2

def run(problem, lines):
    algo = [
        1 if c == '#' else 0
        for c in lines[0].strip()
    ]
    lights = {
        pos
        for pos, v in Grid(lines[2:])
        if v == '#'
    }

    iterations = 2 if problem == 1 else 50

    for iteration in range(iterations):
        lights = apply_algo(lights, algo, iteration)

    return len(lights)

example1 = multiline_lines(r"""
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
""")

run(1, example1) | eq(35)

run(1, input_lines) | debug('Star 1') | eq(5275)

run(2, example1) | eq(3351)

run(2, input_lines) | debug('Star 2') | eq(16482)
