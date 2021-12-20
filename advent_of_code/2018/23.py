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

    def get_group(p):
        queue = [p]
        group = {p}
        seen = set()
        while queue:
            p1 = queue.pop()

            if p1 in seen:
                continue
            seen.add(p1)

            if group <= links[p1]:
                group.add(p1)

            queue += links[p1] - group

        return group

    max_groups = []
    max_group_size = 0

    visited = set()
    for ni in range(len(nanobots)):
        if ni in visited:
            continue

        group = get_group(ni)
        visited |= group

        if max_group_size < len(group):
            max_groups = [group]
            max_group_size = len(group)
        elif max_group_size == len(group):
            max_groups.append(group)

    return max_groups

def get_min_intersection(nanobots, group):
    # TODO
    pass

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

run(2, example2) | eq(36)

run(2, input_lines) | submit(2)
