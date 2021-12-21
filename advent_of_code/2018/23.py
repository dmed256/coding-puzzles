from repo_utils import *

input_lines = get_input_lines()

Nanobot = namedtuple('Nanobot', ['pos', 'r'])

def get_largest_groups(nanobots):
    links = defaultdict(set)
    for ni1 in range(len(nanobots)):
        n1 = nanobots[ni1]
        for ni2 in range(len(nanobots)):
            n2 = nanobots[ni2]
            if pos_distance(n1.pos, n2.pos) <= n1.r + n2.r:
                links[ni1].add(ni2)
                links[ni2].add(ni1)

    def get_largest_groups_for(p1, pairs_visited):
        visited = {p1}
        max_groups = [[p1]]
        for p2 in links[p1]:
            if p2 == p1 or p2 in visited:
                continue

            if (p1, p2) in pairs_visited:
                continue

            pairs_visited.add((p1, p2))
            pairs_visited.add((p2, p1))

            visited.add(p2)

            group = [p1, p2]
            while True:
                nodes = set(links[group[0]])
                for point in group[1:]:
                    nodes &= links[point]
                nodes -= visited

                if not nodes:
                    break

                next_point = min(nodes)

                if (next_point, p1) in pairs_visited:
                    break

                for point in group:
                    pairs_visited.add((point, next_point))
                    pairs_visited.add((next_point, point))

                visited.add(next_point)
                group.append(next_point)

            if len(group) < len(max_groups[0]):
                continue

            if len(group) > len(max_groups[0]):
                max_groups = [group]
                continue

            max_groups.append(group)

        return max_groups

    pairs_visited = set()
    groups = [
        group
        for ni in range(len(nanobots))
        for group in get_largest_groups_for(ni, pairs_visited)
    ]

    max_length = max([
        len(group)
        for group in groups
    ])

    return {
        tuple(sorted(group))
        for group in groups
        if len(group) == max_length
    }

# Find midpoint between the circles and average them all up
# Circles should be convex so we just need to traverse toward (0, 0, 0)
def get_min_intersection(nanobots, group):
    group = set(group)
    print(group)

    # If a circle A completely covers another circle B, there is no
    # need to check whether a point is in A if it's in B
    covers = set()
    for ni1 in range(len(group)):
        n1 = nanobots[ni1]
        for ni2 in range(ni1 + 1, len(group)):
            n2 = nanobots[ni2]

            if pos_distance(n1.pos, n2.pos) + n2.r <= n1.r:
                covers.add(ni1)
                break

    group -= covers

    def get_midpoint(n1, n2, axis):
        _, p1, p2, _ = sorted([
            n1.pos[axis] + n1.r,
            n1.pos[axis] - n1.r,
            n2.pos[axis] + n2.r,
            n2.pos[axis] - n2.r,
        ])
        return (p1 + p2) / 2

    center_points = [[], [], []]
    for ni1 in range(len(group)):
        n1 = nanobots[ni1]
        for ni2 in range(ni1 + 1, len(group)):
            n2 = nanobots[ni2]

            for axis in range(3):
                center_points[axis].append(
                    get_midpoint(n1, n2, axis)
                )

    center = [
        sum(point[axis] for point in center_points) / len(center_points)
        for axis in range(3)
    ]

    # Find grid positions around the probably-not-grid-position center
    grid_centers = [
        (x, y, z)
        for x in {math.floor(center[0]), math.ceil(center[0])}
        for y in {math.floor(center[1]), math.ceil(center[1])}
        for z in {math.floor(center[2]), math.ceil(center[2])}
    ]

    for pos in grid_centers:
        print(sorted([
            max(0, pos_distance(n.pos, pos) - n.r)
            for ni in group
            if (n := nanobots[ni])
        ]))

    def in_group(pos):
        return all(
            pos_distance(n.pos, pos) <= n.r
            for ni in group
            if (n := nanobots[ni])
        )

    # Make sure the grid points are inside all groups since we're
    # approximating
    grid_centers = [
        grid_center
        for grid_center in grid_centers
        if in_group(grid_center)
    ]

    origin = (0, 0, 0)
    def get_distance(pos):
        return pos_distance(pos, origin)

    visited = set()
    queue = heapify([
        (get_distance(pos), pos)
        for pos in grid_centers
    ])
    min_dist = None

    while queue:
        dist, pos = heapq.heappop(queue)

        if pos in visited:
            continue
        visited.add(pos)

        if min_dist and min_dist <= dist:
            continue
        min_dist = dist

        for direction in DIRECTIONS:
            npos = apply_direction(pos, direction)

            if not in_group(npos):
                continue

            ndist = get_distance(npos)
            if ndist < dist:
                heapq.heappush(queue, (ndist, npos))

    return min_dist


def run(problem, lines):
    nanobots = []
    for line in lines:
        left, r = line.split('>, r=')

        r = int(r)
        pos = [int(x) for x in left.split('<')[1].split(',')]
        nanobots.append(Nanobot(pos, r))

    if problem == 1:
        largest_nanobot = max(nanobots, key=lambda n: n.r)
        return len([
            n2
            for n2 in nanobots
            if pos_distance(largest_nanobot.pos, n2.pos) <= largest_nanobot.r
        ])

    print(get_largest_groups(nanobots))

    return min(
        get_min_intersection(nanobots, group)
        for group in get_largest_groups(nanobots)
    )


example1 = multiline_lines(r"""
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1
""")

run(1, example1) | eq(7)

run(1, input_lines) | debug('Star 1') | eq(305)

example2 = multiline_lines(r"""
pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5
""")

# run(2, example2) | eq(36)

# run(2, input_lines) | debug('Star 2')
