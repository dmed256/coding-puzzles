from repo_utils import *

input_lines = get_input_lines()

Nanobot = namedtuple('Nanobot', ['pos', 'r'])


def in_nanobot(n, pos):
    return pos_distance(n.pos, pos) <= n.r


def intersects_bounds(bounds, pos, r):
    x, y, z = pos

    min_x, max_x = bounds[0]
    min_y, max_y = bounds[1]
    min_z, max_z = bounds[2]

    # Find the min-distances to the bounding box
    # for each axis specifically to get the closest
    # point in the cube
    x_dist = max([0, min_x - x, x - max_x])
    y_dist = max([0, min_y - y, y - max_y])
    z_dist = max([0, min_z - z, z - max_z])

    return x_dist + y_dist + z_dist <= r


def get_bounds_corners(bounds):
    return list(
        (x, y, z)
        for x, y, z in itertools.product(*bounds)
    )


def find_intersections(bounds, nanobots):
    return sum([
        intersects_bounds(bounds, n.pos, n.r)
        for n in nanobots
    ])


def bounds_volume(bounds):
    return mult([
        bounds[axis][1] - bounds[axis][0]
        for axis in range(3)
    ])


def run(problem, lines):
    nanobots = []
    for line in lines:
        left, r = line.split('>, r=')

        r = int(r)
        pos = [int(x) for x in left.split('<')[1].split(',')]

        nanobots.append(Nanobot(pos, r))

    if problem == 1:
        largest_n = sorted(
            nanobots,
            key=lambda n: n.r,
            reverse=True,
        )[0]
        return len([
            n2
            for n2 in nanobots
            if in_nanobot(largest_n, n2.pos)
        ])

    # Find max axis value
    max_bound_value = max([
        max(abs(n.pos[axis]) for n in nanobots)
        for axis in range(3)
    ])

    # Get the closes bit representation for clean boxes
    bits = 0
    while max_bound_value:
        max_bound_value >>= 1
        bits += 1

    max_bound_value = 1 << bits
    max_bounds = tuple([
        (-max_bound_value, max_bound_value)
        for axis in range(3)
    ])

    def build_queue_entry(bounds):
        intersections = find_intersections(bounds, nanobots)
        volume = bounds_volume(bounds)

        dist = min([
            abs(x) + abs(y) + abs(z)
            for x, y, z in get_bounds_corners(bounds)
        ])

        # Prioritize counts, then closeness to origin, lastly volume
        h = (-intersections, -dist, -volume)

        return (
            h,
            intersections,
            volume,
            dist,
            bounds,
        )

    queue = [build_queue_entry(max_bounds)]

    max_intersections = None
    min_dist = None

    while queue:
        _, intersections, volume, dist, bounds = heapq.heappop(queue)

        if max_intersections:
            if max_intersections < intersections:
                break
            if max_intersections == intersections and min_dist <= dist:
                break

        if volume == 1:
            for pos in get_bounds_corners(bounds):
                pos_dist = pos_distance(pos, (0, 0, 0))
                pos_intersections = sum([
                    pos_distance(pos, n.pos) <= n.r
                    for n in nanobots
                ])

                if max_intersections is None or max_intersections < pos_intersections:
                    max_intersections = pos_intersections
                    min_dist = pos_dist
                elif max_intersections == pos_intersections:
                    min_dist = safe_min(min_dist, pos_dist)
            continue

        mids = [
            (bounds[axis][0] + bounds[axis][1]) // 2
            for axis in range(3)
        ]
        new_axis_bounds = [
            [(bounds[axis][0], mids[axis]), (mids[axis], bounds[axis][1])]
            for axis in range(3)
        ]
        for bounds in itertools.product(*new_axis_bounds):
            heapq.heappush(queue, build_queue_entry(bounds))

    return min_dist

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

run(2, example2) | eq(36)

run(2, input_lines) | debug('Star 2')
