from repo_utils import *

input_lines = get_input_lines()

def get_grid_values(problem, lines):
    grid_values = [
        [int(x) for x in line]
        for line in lines
    ]
    if problem == 1:
        return grid_values

    rows = len(grid_values)
    cols = len(grid_values[0])

    return [
        [
            1 + ((grid_values[r][c] - 1 + row_tile + col_tile) % 9)
            for col_tile in range(5)
            for c in range(cols)
        ]
        for row_tile in range(5)
        for r in range(rows)
    ]

def run(problem, lines):
    grid_values = get_grid_values(problem, lines)

    grid = Grid(grid_values)
    grid2 = Grid([
        [None for x in row]
        for row in grid_values
    ])

    start = (0, 0)
    end = (grid.width - 1, grid.height - 1)

    queue = [(0, start)]
    while queue:
        risk, pos = heapq.heappop(queue)

        # Check that we haven't visited this node with less risk
        if grid2[pos] and grid2[pos] <= risk:
            continue

        grid2[pos] = risk

        for npos in grid.neighbors(pos):
            new_risk = risk + grid[npos]

            if grid2[npos] and grid2[npos] <= new_risk:
                continue

            # Add the next node based on distance heuristic
            heapq.heappush(queue, (new_risk, npos))

    return grid2[end]

example1 = multiline_lines(r"""
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
""")

run(1, example1) | eq(40)

run(1, input_lines) | debug('Star 1') | eq(435)

run(2, example1) | eq(315)

run(2, input_lines) | debug('Star 2') | eq(2842)
