from repo_utils import *

input_lines = get_input_lines()

Nanobot = namedtuple('Nanobot', ['pos', 'r'])

def in_nanobot(n, pos):
    return pos_distance(n.pos, pos) <= n.r

def bounds_volume(bounds):
    return mult([
        bound[1] - bound[2]
        for bound in bounds
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
        intersections = find_intersections(bounds)
        volume = bounds_volume(bounds)

        # TODO: HERE
        h = ()

        return (
            h,
            intersections,
            volume,
            bounds,
        )

    queue = [build_queue_entry(max_bounds)]

    while queue:
        neg_count, vol, bounds = heapq.heappop(queue)
        max

        if vol == 1:
            break

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

# run(1, example1) | eq(7)

# run(1, input_lines) | debug('Star 1') | eq(305)

example2 = multiline_lines(r"""
pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5
""")

# run(2, example2) | eq(36)

# High: 82444725
# High: 82444619
# High: 82444690
#       78687692
run(2, input_lines) | debug('Star 2')
