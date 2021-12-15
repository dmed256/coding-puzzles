import numpy as np
from repo_utils import *

input_lines = get_input_lines()

def get_key_path(grid, pos1, pos2):
    gates = set(string.ascii_uppercase)
    queue = [(0, pos1, set())]
    visited = {pos1}

    while queue:
        steps, pos, keys_needed = heapq.heappop(queue)

        for npos in grid.neighbors(pos):
            next_steps = steps + 1

            if npos == pos2:
                return (next_steps, keys_needed)

            if npos in visited:
                continue
            visited.add(npos)

            v = grid[npos]
            if v == '#':
                continue

            next_keys_needed = deepcopy(keys_needed)
            if v in gates:
                next_keys_needed.add(v.lower())

            heapq.heappush(queue, (next_steps, npos, next_keys_needed))

def run(problem, lines):
    grid = Grid(lines)
    start_pos = grid.first('@')

    key_positions = {
        v: pos
        for pos, v in grid
        if v in string.ascii_lowercase
    }
    all_keys = set(key_positions.keys())

    start_positions = {}
    if problem == 1:
        grid[start_pos] = '0'
        start_positions['0'] = start_pos
    else:
        start_keys = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                npos = (start_pos[0] + dx, start_pos[1] + dy)
                grid[npos] = '#'

        for i, (dx, dy) in enumerate([(-1, -1), (-1, 1), (1, -1), (1, 1)]):
            key_pos = (start_pos[0] + dx, start_pos[1] + dy)
            start_key = str(i)

            grid[key_pos] = start_key
            start_positions[start_key] = key_pos

    paths = {}
    for k1 in [*start_positions.keys(), *key_positions.keys()]:
        pos1 = start_positions.get(k1, key_positions.get(k1))
        for k2 in key_positions.keys():
            if k1 == k2 or (k1, k2) in paths:
                continue

            pos2 = key_positions[k2]

            path = get_key_path(grid, pos1, pos2)
            if path is None:
                continue

            paths[(k1, k2)] = path
            paths[(k2, k1)] = path

    def heuristic(steps, keys_captured):
        return (-len(keys_captured), steps)

    queue = [(
        heuristic(0, set()),
        0,
        tuple(start_positions.keys()),
        set(),
    )]
    min_steps = {}
    min_ans = None
    while queue:
        _, steps, positions, keys_captured = heapq.heappop(queue)

        if min_ans and min_ans <= steps:
            continue

        min_step_key = (positions, tuple(sorted(keys_captured)))
        if min_step_key in min_steps and min_steps[min_step_key] <= steps:
            continue
        min_steps[min_step_key] = steps

        if all_keys == keys_captured:
            min_ans = safe_min(min_ans, steps)
            continue

        for pos_idx, pos in enumerate(positions):
            for key in all_keys - keys_captured:
                path_key = (pos, key)
                if path_key not in paths:
                    continue

                path_steps, keys_needed = paths[path_key]
                if not (keys_needed <= keys_captured):
                    continue

                next_positions = list(positions)
                next_positions[pos_idx] = key
                next_positions = tuple(next_positions)

                next_steps = steps + path_steps
                next_keys_captured = keys_captured | {key}
                next_h = heuristic(next_steps, next_keys_captured)

                heapq.heappush(
                    queue,
                    (next_h, next_steps, next_positions, next_keys_captured),
                )

    return min_ans


example1 = multiline_lines(r"""
#########
#b.A.@.a#
#########
""")

example2 = multiline_lines(r"""
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
""")

example3 = multiline_lines(r"""
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
""")

example4 = multiline_lines(r"""
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
""")

example5 = multiline_lines(r"""
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
""")

run(1, example1) | eq(8)
run(1, example2) | eq(86)
run(1, example3) | eq(132)
run(1, example4) | eq(136)
run(1, example5) | eq(81)

run(1, input_lines) | debug('Star 1') | eq(5964)

example1 = multiline_lines(r"""
#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######
""")

example2 = multiline_lines(r"""
###############
#d.ABC.#.....a#
###############
#######@#######
###############
#b.....#.....c#
###############
""")

example3 = multiline_lines(r"""
#############
#DcBa.#.GhKl#
#.#######I###
#e#d##@##j#k#
###C#######J#
#fEbA.#.FgHi#
#############
""")

example4 = multiline_lines(r"""
#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba###BcIJ#
######@######
#nK.L###G...#
#M###N#H###.#
#o#m..#i#jk.#
#############
""")

run(2, example1) | eq(8)
run(2, example2) | eq(24)
run(2, example3) | eq(32)
run(2, example4) | eq(72)

run(2, input_lines) | debug('Star 2') | eq(1996)
