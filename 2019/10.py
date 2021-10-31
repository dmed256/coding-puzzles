import re
import math
from advent_of_code import *

def get_asteroids(lines):
    asteroids = []
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                asteroids.append([x, y])

    return asteroids

def find_asteroid_locations(asteroids, asteroid):
    [x, y] = asteroid
    locations = {}
    for [x2, y2] in asteroids:
        if [x, y]  == [x2, y2]:
            continue

        dy = y2 - y
        dx = x2 - x
        distance = math.sqrt(dx*dx + dy*dy)

        hpi = 0.5 * math.pi
        degree = math.atan2(dy, dx)
        if -hpi <= degree <= 0:
            # Q1
            degree = degree
        elif degree < -hpi:
            # Q4
            degree = 1000 + degree
        else:
            # Q2 + Q3
            degree = 10 + degree

        info = locations.get(degree, [])
        info.append([distance, [x2, y2]])
        info.sort(key=lambda i: i[0])

        locations[degree] = info

    return locations

def run(lines):
    asteroids = get_asteroids(lines)

    max_asteroid = asteroids[0]
    max_count = 0
    for asteroid in asteroids:
        locations = find_asteroid_locations(asteroids, asteroid)
        count = len(locations)
        if max_count < count:
            max_asteroid = asteroid
            max_count = count

    return [max_asteroid, max_count]

example1 = multiline_lines("""
.#..#
.....
#####
....#
...##
""")

example2 = multiline_lines("""
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
""")

example3 = multiline_lines("""
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
""")

example4 = multiline_lines("""
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
""")

example5 = multiline_lines("""
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
""")

run(example1) | eq([[3, 4], 8])
run(example2) | eq([[5, 8], 33])
run(example3) | eq([[1, 2], 35])
run(example4) | eq([[6, 3], 41])
run(example5) | eq([[11, 13], 210])

input_lines = get_input_lines()

run(input_lines) | debug('Star 1')

def run2(lines, station_coords, target_asteroid):
    # 1-index -> 0-index
    target_asteroid -= 1

    asteroids = get_asteroids(lines)
    locations = find_asteroid_locations(asteroids, station_coords)

    print_grid = False
    if print_grid:
        [x, y] = station_coords
        pixels = [
            [blue(c) for c in line]
            for line in lines
        ]
        pixels[y][x] = yellow('x')

    ordered_degrees = sorted(locations.keys())
    evaporated_asteroids = []
    while len(evaporated_asteroids) <= target_asteroid:
        for degree in ordered_degrees:
            if not locations[degree]:
                continue
            [distance, asteroid] = locations[degree].pop(0)
            evaporated_asteroids.append(asteroid)

            if print_grid:
                [x, y] = asteroid
                pixels[y][x] = green('*')
                print('\n'.join([
                    ' '.join(row)
                    for row in pixels
                ]))
                pixels[y][x] = red('*')
                print()
                input()

    return evaporated_asteroids[target_asteroid]

run2(example5, [11, 13], 1) | eq([11, 12])
run2(example5, [11, 13], 2) | eq([12, 1])
run2(example5, [11, 13], 3) | eq([12, 2])
run2(example5, [11, 13], 10) | eq([12, 8])
run2(example5, [11, 13], 20) | eq([16, 0])
run2(example5, [11, 13], 50) | eq([16, 9])
run2(example5, [11, 13], 100) | eq([10, 16])
run2(example5, [11, 13], 199) | eq([9, 6])
run2(example5, [11, 13], 200) | eq([8, 2])
run2(example5, [11, 13], 201) | eq([10, 9])
run2(example5, [11, 13], 299) | eq([11, 1])

[x, y] = run2(input_lines, [13, 17], 200)
(100*x + y)| debug('Star 2')
