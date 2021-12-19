from repo_utils import *

ROCKY = 0
WET = 1
NARROW = 2

TORCH = 1 << 0
CLIMBING_GEAR = 1 << 1

terrain_items_required = {
    ROCKY: {
        TORCH,
        CLIMBING_GEAR,
        TORCH | CLIMBING_GEAR,
    },
    WET: {
        0,
        CLIMBING_GEAR,
    },
    NARROW: {
        0,
        TORCH,
    },
}

items_to_move = {
    (t1, t2): terrain_items_required[t1] & terrain_items_required[t2]
    for t1 in [ROCKY, WET, NARROW]
    for t2 in [ROCKY, WET, NARROW]
}

@functools.cache
def get_geologic_index(depth, x, y):
    if x == 0:
        return (y * 48271)

    if y == 0:
        return (x * 16807)

    return (
        get_erotion_level(depth, x - 1, y)
        * get_erotion_level(depth, x, y - 1)
    )

@functools.cache
def get_erotion_level(depth, x, y):
    geologic_index = get_geologic_index(depth, x, y)

    return (geologic_index + depth) % 20183

def run(problem, depth, target):
    max_x = target[0] + 1
    max_y = target[1] + 1

    padding = 100

    grid = Grid([
        [0 for x in range(max_x + padding)]
        for y in range(max_y + padding)
    ])

    for pos, _ in grid:
        x, y = pos
        grid[pos] = get_erotion_level(depth, x, y) % 3

    grid[target] = ROCKY

    if problem == 1:
        return sum(
            grid[(x, y)]
            for y in range(max_y)
            for x in range(max_x)
        )

    def heuristic(pos):
        return pos_distance(pos, target)

    def build_entry(pos, minutes, items):
        return (
            minutes + heuristic(pos),
            minutes,
            pos,
            items
        )

    queue = [build_entry((0, 0), 0, TORCH)]
    D = defaultdict(int)
    min_minutes = None
    while queue:
        _, minutes, pos, items = heapq.heappop(queue)

        if min_minutes and min_minutes <= minutes:
            continue

        if pos == target:
            if not items & TORCH:
                minutes += 7
            min_minutes = safe_min(min_minutes, minutes)
            continue

        key = (pos, items)
        if key in D and D[key] < minutes:
            continue
        D[key] = minutes

        t1 = grid[pos]
        for npos in grid.neighbors(pos):
            t2 = grid[npos]

            for next_items in items_to_move[(t1, t2)]:
                if items == next_items:
                    next_minutes = minutes + 1
                else:
                    next_minutes = minutes + 8

                key = (npos, next_items)
                if key in D and D[key] <= next_minutes:
                    continue
                D[key] = next_minutes

                heapq.heappush(
                    queue,
                    build_entry(npos, next_minutes, next_items),
                )

    return min_minutes

run(1, 510, (10, 10)) | eq(114)

run(1, 3558, (15, 740)) | debug('Star 1') | eq(11810)

run(2, 510, (10, 10)) | eq(45)

run(2, 3558, (15, 740)) | debug('Star 2') | eq(1015)
