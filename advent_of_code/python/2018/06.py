from repo_utils import *

input_lines = get_input_lines()

def parse_lines(lines):
    coords = [
        [int(x) for x in line.split(', ')]
        for line in lines
    ]

    min_x = min(p[0] for p in coords)
    max_x = max(p[0] for p in coords)
    min_y = min(p[1] for p in coords)
    max_y = max(p[1] for p in coords)

    return coords, (min_x, max_x), (min_y, max_y)

def run(lines):
    coords, (min_x, max_x), (min_y, max_y) = parse_lines(lines)

    min_dist = {}
    owners = defaultdict(list)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            pos = (x, y)
            for ci, (cx, cy) in enumerate(coords):
                dist = abs(x - cx) + abs(y - cy)

                if pos not in min_dist or dist < min_dist[pos]:
                    min_dist[pos] = dist
                    owners[pos] = [ci]
                elif dist == min_dist[pos]:
                    min_dist[pos] = dist
                    owners[pos].append(ci)

    # Remove duplicates
    owners = {
        pos: point_owners[0]
        for pos, point_owners in owners.items()
        if len(point_owners) == 1
    }

    # Find owners that have infinite areas
    infinity_owners = set()
    for (x, y), owner in owners.items():
        if x in [min_x, max_x] or y in [min_y, max_y]:
            infinity_owners.add(owner)

    areas = Counter()
    for pos, owner in owners.items():
        if owner in infinity_owners:
            continue
        areas[owner] += 1

    return areas.most_common()[0][1]

def run2(lines, max_dist):
    coords, (min_x, max_x), (min_y, max_y) = parse_lines(lines)

    x_coords = [x for x, y in coords]
    y_coords = [y for x, y in coords]

    mid_pos = ((min_x + max_x) // 2, (min_y + max_y) // 2)
    queue = deque([mid_pos])
    visited = set([mid_pos])
    region_size = 1
    while queue:
        pos = queue.popleft()
        for direction in DIRECTIONS:
            npos = apply_direction(pos, direction)
            if npos in visited:
                continue

            visited.add(npos)

            dist = (
                sum(abs(npos[0] - x) for x in x_coords)
                + sum(abs(npos[1] - y) for y in y_coords)
            )
            if dist >= max_dist:
                continue

            region_size += 1
            queue.append(npos)

    return region_size


example1 = multiline_lines(r"""
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
""")

run(example1) | eq(17)

run(input_lines) | debug('Star 1') | eq(2906)

run2(example1, 32) | eq(16)

run2(input_lines, 10000) | debug('Star 2') | eq(50530)
