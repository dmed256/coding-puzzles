from repo_utils import *

input_lines = get_input_lines()

def get_path(grid, pos1, pos2):
    queue = [(0, pos1)]
    visited = {pos1}

    while queue:
        steps, pos = heapq.heappop(queue)

        for npos in grid.neighbors(pos):
            next_steps = steps + 1

            if npos == pos2:
                return next_steps

            if npos in visited:
                continue
            visited.add(npos)

            v = grid[npos]
            if v != '.':
                continue

            heapq.heappush(queue, (next_steps, npos))

def run(problem, lines):
    grid = Grid(lines, default_value=' ')

    x_ends = {0, grid.width - 1}
    y_ends = {0, grid.height - 1}

    def get_gate_pos(pos1, pos2):
        is_outer = any((
            pos1[0] in x_ends,
            pos2[0] in x_ends,
            pos1[1] in y_ends,
            pos2[1] in y_ends,
        ))

        for p1, p2 in [(pos1, pos2), (pos2, pos1)]:
            for direction in GRID_DIRECTIONS:
                if grid.apply_direction(p1, direction) != p2:
                    continue

                p3 = grid.apply_direction(p2, direction)
                if p3 is None or grid[p3] != '.':
                    continue

                gate_key = ''.join(sorted(grid[p1] + grid[p2]))
                return (is_outer, gate_key, p3)

    gate_values = set(string.ascii_uppercase)
    gates = {}
    for pos, v in grid:
        if v not in gate_values:
            continue

        for npos in grid.neighbors(pos):
            v2 = grid[npos]
            if v2 not in gate_values:
                continue

            is_outer, gate_key, gate_pos = get_gate_pos(pos, npos)

            # Get a 1-char ID and store it
            gates[(gate_key, is_outer)] = gate_pos

            # Clean up the grid
            grid[pos] = ' '
            grid[npos] = ' '
            grid[gate_pos] = gate_key

    paths = defaultdict(dict)
    for gate1 in gates.keys():
        gate_key1, is_outer1 = gate1
        pos1 = gates[gate1]

        for gate2 in gates.keys():
            gate_key2, is_outer2 = gate2
            pos2 = gates[gate2]

            if gate1 == gate2 or (gate1, gate2) in paths:
                continue

            steps = get_path(grid, pos1, pos2)
            if steps is None:
                continue

            if gate_key2 != 'AA':
                paths[gate1][gate2] = steps

            if gate_key2 != 'AA':
                paths[gate2][gate1] = steps

    start = ('AA', True)
    start_pos, _ = gates[start]

    end = ('ZZ', True)
    end_pos, _ = gates[end]

    queue = [(0, 0, start)]
    min_dist = None
    while queue:
        depth, steps, gate = heapq.heappop(queue)

        if min_dist and min_dist <= steps:
            continue

        for gate2, dist in paths[gate].items():
            next_steps = steps + dist

            if gate2 == end:
                if depth == 0:
                    min_dist = safe_min(min_dist, next_steps)
                continue

            # Takes 1 step to go through the portal
            next_steps += 1

            gate_key2, is_outer2 = gate2

            # Can't go up any higher
            if problem == 2 and depth == 0 and is_outer2:
                continue

            next_depth = depth
            if problem == 2:
                if is_outer2:
                    next_depth -= 1
                else:
                    next_depth += 1

            next_gate = (gate_key2, not is_outer2)

            heapq.heappush(queue, (next_depth, next_steps, next_gate))

    return min_dist

example1 = multiline_lines(r"""
         A
         A
  #######.#########
  #######.........#
  #######.#######.#
  #######.#######.#
  #######.#######.#
  #####  B    ###.#
BC...##  C    ###.#
  ##.##       ###.#
  ##...DE  F  ###.#
  #####    G  ###.#
  #########.#####.#
DE..#######...###.#
  #.#########.###.#
FG..#########.....#
  ###########.#####
             Z
             Z
""")

example2 = multiline_lines(r"""
                   A
                   A
  #################.#############
  #.#...#...................#.#.#
  #.#.#.###.###.###.#########.#.#
  #.#.#.......#...#.....#.#.#...#
  #.#########.###.#####.#.#.###.#
  #.............#.#.....#.......#
  ###.###########.###.#####.#.#.#
  #.....#        A   C    #.#.#.#
  #######        S   P    #####.#
  #.#...#                 #......VT
  #.#.#.#                 #.#####
  #...#.#               YN....#.#
  #.###.#                 #####.#
DI....#.#                 #.....#
  #####.#                 #.###.#
ZZ......#               QG....#..AS
  ###.###                 #######
JO..#.#.#                 #.....#
  #.#.#.#                 ###.#.#
  #...#..DI             BU....#..LF
  #####.#                 #.#####
YN......#               VT..#....QG
  #.###.#                 #.###.#
  #.#...#                 #.....#
  ###.###    J L     J    #.#.###
  #.....#    O F     P    #.#...#
  #.###.#####.#.#####.#####.###.#
  #...#.#.#...#.....#.....#.#...#
  #.#####.###.###.#.#.#########.#
  #...#.#.....#...#.#.#.#.....#.#
  #.###.#####.###.###.#.#.#######
  #.#.........#...#.............#
  #########.###.###.#############
           B   J   C
           U   P   P
""")

run(1, example1) | eq(23)
run(1, example2) | eq(58)

run(1, input_lines) | debug('Star 1') | eq(642)

example1 = multiline_lines(r"""
             Z L X W       C
             Z P Q B       K
  ###########.#.#.#.#######.###############
  #...#.......#.#.......#.#.......#.#.#...#
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###
  #.#...#.#.#...#.#.#...#...#...#.#.......#
  #.###.#######.###.###.#.###.###.#.#######
  #...#.......#.#...#...#.............#...#
  #.#########.#######.#.#######.#######.###
  #...#.#    F       R I       Z    #.#.#.#
  #.###.#    D       E C       H    #.#.#.#
  #.#...#                           #...#.#
  #.###.#                           #.###.#
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#
CJ......#                           #.....#
  #######                           #######
  #.#....CK                         #......IC
  #.###.#                           #.###.#
  #.....#                           #...#.#
  ###.###                           #.#.#.#
XF....#.#                         RF..#.#.#
  #####.#                           #######
  #......CJ                       NM..#...#
  ###.#.#                           #.###.#
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#
  #.....#        F   Q       P      #.#.#.#
  ###.###########.###.#######.#########.###
  #.....#...#.....#.......#...#.....#.#...#
  #####.#.###.#######.#######.###.###.#.#.#
  #.......#.......#.#.#.#.#...#...#...#.#.#
  #####.###.#####.#.#.#.#.###.###.#.###.###
  #.......#.....#.#...#...............#...#
  #############.#.#.###.###################
               A O F   N
               A A D   M
""")

run(2, example1) | eq(396)
run(2, input_lines) | debug('Star 2') | eq (7492)
