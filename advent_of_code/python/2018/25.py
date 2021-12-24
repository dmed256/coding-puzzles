from repo_utils import *

input_lines = get_input_lines()

def run(problem, lines):
    points = [
        tuple([int(x) for x in line.split(',')])
        for line in lines
    ]

    links = defaultdict(set)
    for p1 in points:
        for p2 in points:
            if p1 == p2:
                continue

            if pos_distance(p1, p2) <= 3:
                links[p1].add(p2)
                links[p2].add(p1)

    def get_constellation(p):
        queue = [p]
        constellation = {p}
        while queue:
            p1 = queue.pop()

            missing = links[p1] - constellation
            constellation |= missing

            queue += list(missing)

        return constellation

    points = set(points)
    constellations = []
    while points:
        p = min(points)
        constellation = get_constellation(p)

        points -= constellation
        constellations.append(constellation)

    return len(constellations)

example1 = multiline_lines(r"""
 0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0
""")

example2 = multiline_lines(r"""
-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0
""")

example3 = multiline_lines(r"""
1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2
""")

example4 = multiline_lines(r"""
1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2
""")

run(1, example1) | eq(2)
run(1, example2) | eq(4)
run(1, example3) | eq(3)
run(1, example4) | eq(8)

run(1, input_lines) | debug('Star 1') | eq(388)
