import numpy as np
from advent_of_code import *

def get_graph_type(value):
    if value == '#':
        return Graph.Type.WALL
    if value == '.':
        return Graph.Type.NOTHING
    return Graph.Type.OBJECT

def run(lines):
    grid = Grid(lines)
    graph = Graph(
        grid,
        get_type=get_graph_type
    )

    start_pos = grid.first('@')

    key_positions_map = {
        letter: pos
        for pos, letter in graph.pos_to_object.items()
        if letter.isalpha() and letter.islower()
    }
    key_positions = set(key_positions_map.values())
    keys = set(key_positions_map.keys())

    key_paths = {
        key: graph.find_paths(
            key_pos,
            key_positions - set([key_pos]),
        )
        for key, key_pos in key_positions_map.items()
    }

    # Hack to reuse key logic with '@' starting position
    key_paths['@'] = graph.find_paths(start_pos, key_positions)
    key_positions_map['@'] = start_pos

    key_deps = {
        (key, target_key): set([
            value.lower()
            for node in path
            if (value := grid[node]).isupper()
            and value.lower() != key
        ])
        for key in ['@', *keys]
        for path in key_paths[key]
        if (target_key := grid[path[-1]])
    }

    # print(f'key_paths = {key_paths}')
    # print(f'key_deps = {key_deps}')

    cached_paths = {}
    def find_min_path(key, captured_keys):
        if captured_keys == keys:
            return []

        paths = key_paths[key]

        min_next_path = None
        for path in paths:
            target_key = grid[path[-1]]
            if target_key in captured_keys:
                continue

            deps = key_deps[(key, target_key)]
            # We can't access the key since there are
            # unopened doors in the way
            if deps - captured_keys:
                continue

            cache_key = (key, target_key, *captured_keys)
            reverse_cache_key = (target_key, key, *captured_keys)
            if cache_key not in cached_paths:
                next_path = find_min_path(
                    target_key,
                    captured_keys | set([target_key]),
                )
                if next_path is None:
                    continue
                cached_paths[cache_key] = next_path
                cached_paths[reverse_cache_key] = next_path
            else:
                next_path = cached_paths[cache_key]

            next_path = [*path, *next_path]

            if min_next_path is None or len(next_path) < len(min_next_path):
                min_next_path = next_path

        return min_next_path

    grid.print()
    tic()
    min_path = find_min_path('@', captured_keys=set())
    toc('')

    return len(min_path)

example1 = multiline_lines("""
#########
#b.A.@.a#
#########
""")

example2 = multiline_lines("""
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
""")

example3 = multiline_lines("""
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
""")

example4 = multiline_lines("""
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

example5 = multiline_lines("""
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
""")

# run(example1) | eq(8)
# run(example2) | eq(86)
# run(example3) | eq(132)
# run(example4) | eq(136)
# run(example5) | eq(81)

input_lines = get_input_lines()
run(input_lines) | debug('Star 1')