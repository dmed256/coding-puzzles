from repo_utils import *

input_lines = get_input_lines()

Nanobot = namedtuple('Nanobot', ['pos', 'r'])

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

    pass
    # max_count = 0
    # for n1 in nanobots:
    #     max_count = max(max_count, len([
    #         n2
    #         for n2 in nanobots
    #         if pos_distance(n1.pos, n2.pos) <= n1.r
    #     ]))

    # return max_count

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

# run(2, input_lines) | submit(2)
