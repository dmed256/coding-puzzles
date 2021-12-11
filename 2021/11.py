from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

def run(problem, lines):
    grid = Grid([
        [int(c) for c in line]
        for line in lines
    ])

    flash_count = 0
    step = 0
    while True:
        flash_queue = []
        flashed = set()
        for (pos, v) in grid:
            if v >= 9:
                grid[pos] = 0
                flash_queue.append(pos)
            else:
                grid[pos] += 1

        while flash_queue:
            pos = flash_queue.pop()
            if pos in flashed:
                continue
            flashed.add(pos)
            for n in grid.neighbors(pos, DIAG_DIRECTIONS):
                if grid[n] == 0:
                    continue

                grid[n] += 1
                if grid[n] > 9:
                    grid[n] = 0
                    flash_queue.append(n)

        flash_count += len(flashed)
        step += 1

        if problem == 1:
            if step == 100:
                return flash_count
        else:
            if len(flashed) == 100:
                return step

example1 = multiline_lines(r"""
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
""")

run(1, example1) | eq(1656)

run(1, input_lines) | debug('Star 1') | eq(1697)

run(2, example1) | eq(195)

run(2, input_lines) | debug('Star 2') | eq(344)
