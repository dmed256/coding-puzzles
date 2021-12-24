from repo_utils import *

def run(problem, number, destination):
    def is_wall(x, y):
        val = x*x + 3*x + 2*x*y + y + y*y
        val += number
        val = bit_count(val)
        return val % 2

    dest_x, dest_y = destination

    grid = Grid([
        [
            '#' if is_wall(x, y) else '.'
            for x in range(dest_x + 100)
        ]
        for y in range(dest_y + 100)
    ])

    grid[destination] = '*'

    queue = [((1, 1), 0)]
    visited = set([(1, 1)])
    less_than_50 = set([(1, 1)])
    while queue:
        pos, steps = queue.pop(0)

        if problem == 1:
            if pos == destination:
                return steps
        else:
            if steps > 50:
                return len(less_than_50)

        for n in grid.neighbors(pos):
            if n in visited or grid[n] == '#':
                continue

            queue.append((n, steps + 1))
            visited.add(n)
            if steps + 1 <= 50:
                less_than_50.add(n)

run(1, 10, (7, 4)) | eq(11)

run(1, 1352, (31,39)) | debug('Star 1') | eq(90)

run(2, 1352, (31,39)) | debug('Star 2') | eq(135)
