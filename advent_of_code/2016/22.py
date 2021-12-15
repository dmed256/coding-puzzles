from repo_utils import *

input_lines = get_input_lines()

def parse_lines(lines):
    nodes = {}
    for line in lines[2:]:
        node, size, used, _avail, _perc = [x.strip() for x in line.split()]

        x, y = node.replace('/dev/grid/node-x', '').split('-y')
        x = int(x)
        y = int(y)

        size = int(size[:-1])
        used = int(used[:-1])

        nodes[(x, y)] = (used, size)

    return nodes


def run(lines):
    nodes = parse_lines(lines)

    infos = list(nodes.values())
    pairs = 0
    for i in range(len(infos)):
        used1, size1 = infos[i]
        avail1 = size1 - used1
        for j in range(i + 1, len(infos)):
            used2, size2 = infos[j]
            avail2 = size2 - used2
            if used1 and used1 < avail2:
                pairs += 1
            if used2 and used2 < avail1:
                pairs += 1

    return pairs


def empty_to_pos_steps(grid, empty_pos, data_pos, end):
    queue = deque([(empty_pos, 0)])
    visited = {empty_pos, data_pos}
    while queue:
        pos, steps = queue.popleft()
        _, size = grid[pos]

        found_data = False
        for npos in grid.neighbors(pos):
            if npos in visited:
                continue

            used, _ = grid[npos]
            if used > size:
                continue

            if npos == end:
                return steps + 1

            queue.append((npos, steps + 1))
            visited.add(npos)

    return None


def run2(lines):
    nodes = parse_lines(lines)

    grid = Grid.from_points(nodes.keys())
    for pos, info in nodes.items():
        grid[pos] = info

    for pos, (used, size) in grid:
        if used == 0:
            empty_pos = pos
            break

    goal_pos = (0, 0)

    data_pos = (grid.width - 1, 0)
    data_size, _ = grid[data_pos]

    data_neighbor1 = (grid.width - 2, 0)
    data_neighbor2 = (grid.width - 1, 1)

    queue = [
        (empty_pos, data_pos, data_neighbor1, 0),
        (empty_pos, data_pos, data_neighbor2, 0),
    ]
    min_steps = None
    cached_steps = {}

    def queue_key(entry):
        empty_pos, data_pos, next_pos, steps = entry
        dist = abs(data_pos[0] - goal_pos[0]) + abs(data_pos[1] - goal_pos[1])
        return (dist, steps)

    while queue:
        empty_pos, data_pos, next_pos, steps = queue.pop(0)

        if min_steps and min_steps <= steps:
            continue

        # Make sure there's space for the data to move to
        _, node_space = grid[next_pos]
        if data_size > node_space:
            continue

        key = (data_pos, next_pos)
        if key in cached_steps and cached_steps[key] <= steps:
            continue
        cached_steps[key] = steps

        steps_taken = empty_to_pos_steps(grid, empty_pos, data_pos, next_pos)
        if steps_taken is None:
            continue

        # Move empty space to next_pos, then swap data with empty_space
        steps += steps_taken + 1

        if next_pos == goal_pos:
            min_steps = safe_min(min_steps, steps)
            continue

        empty_pos = data_pos
        data_pos = next_pos
        for npos in grid.neighbors(data_pos):
            entry = (empty_pos, data_pos, npos, steps)
            insort_right(queue, entry, key=queue_key)

    return min_steps


example1 = multiline_lines(r"""
root@ebhq-gridcenter# df -h
Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%
""")

run(input_lines) | debug('Star 1') | eq(1045)

run2(example1) | eq(7)

run2(input_lines) | debug('Star 2') | eq(265)
