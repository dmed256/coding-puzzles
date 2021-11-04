import numpy as np
from advent_of_code import *

class KeyGraph:
    def __init__(self, grid, start_pos):
        self.graph = Graph(
            grid,
            start_pos=start_pos,
            get_type=KeyGraph.get_graph_type,
        )

        key_positions_map = {
            letter: pos
            for pos, letter in self.graph.pos_to_object.items()
            if letter.isalpha() and letter.islower()
        }
        key_positions = set(key_positions_map.values())
        self.keys = set(key_positions_map.keys())

        self.key_paths = {
            key: self.graph.find_paths(
                key_pos,
                key_positions - set([key_pos]),
            )
            for key, key_pos in key_positions_map.items()
        }

        # Hack to reuse key logic with '@' starting position
        self.key_paths['@'] = self.graph.find_paths(start_pos, key_positions)

        self.key_deps = {
            (key, target_key): set([
                value.lower()
                for node in path
                if (value := grid[node]).isupper()
                and value.lower() != key
            ])
            for key in ['@', *self.keys]
            for path in self.key_paths[key]
            if (target_key := grid[path[-1]])
        }

    @staticmethod
    def get_graph_type(value):
        if value == '#':
            return Graph.Type.WALL
        if value == '.':
            return Graph.Type.NOTHING
        return Graph.Type.OBJECT

class Problem:
    def __init__(self, lines, problem):
        self.setup_grid(lines, problem)
        self.grid.print()

        self.graphs = [
            KeyGraph(self.grid, start_pos)
            for start_pos in self.start_positions
        ]
        self.keys = set()
        for graph in self.graphs:
            self.keys.update(graph.keys)

    def setup_grid(self, lines, problem):
        self.grid = Grid(lines)
        start_pos = self.grid.first('@')

        if problem == 1:
            self.start_positions = [start_pos]
            return

        (x, y) = start_pos
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                self.grid[(x + dx, y + dy)] = '#'

        self.start_positions = [
            (x + dx, y + dy)
            for dy in [-1, 1]
            for dx in [-1, 1]
        ]

        for pos in self.start_positions:
            self.grid[pos] = '@'

    def find_min_path(self, keys, captured_keys, cached_paths):
        if captured_keys == self.keys:
            return []

        cache_key = ('fmp', *keys, *captured_keys)
        if cache_key not in cached_paths:
            min_path = shortest_list(
                self.find_graph_min_path(
                    graph,
                    graph_idx,
                    keys,
                    captured_keys,
                    cached_paths,
                )
                for graph_idx, graph in enumerate(self.graphs)
            )
            cached_paths[cache_key] = min_path
        else:
            min_path = cached_paths[cache_key]

        return min_path

    def find_graph_min_path(self, graph, graph_idx, keys, captured_keys, cached_paths):
        key = keys[graph_idx]

        if captured_keys == self.keys:
            return []

        paths = graph.key_paths[key]

        min_path = None
        for path in paths:
            target_key = self.grid[path[-1]]
            if target_key in captured_keys:
                continue

            deps = graph.key_deps[(key, target_key)]
            # We can't access the key since there are
            # unopened doors in the way
            if deps - captured_keys:
                continue

            cache_key = ('fgmp', key, target_key, *keys, *captured_keys)
            if cache_key not in cached_paths:
                target_keys = keys.copy()
                target_keys[graph_idx] = target_key

                next_path = self.find_min_path(
                    target_keys,
                    captured_keys | set([target_key]),
                    cached_paths,
                )
                cached_paths[cache_key] = next_path
            else:
                next_path = cached_paths[cache_key]

            if next_path is None:
                continue

            min_path = shortest_list([min_path, [*path, *next_path]])

        return min_path

    def print_path(self, path):
        grid = self.grid.copy()
        graph_pos = self.start_positions.copy()

        keys = set()
        last_pos = None
        for pos in path:
            graph_idx = [
                i
                for i, n in enumerate(graph_pos)
                if pos in grid.neighbors(n)
            ][0]

            value = grid[pos]
            if value.islower():
                keys.add(value)
                door_pos = grid.first(value.upper())
                if door_pos:
                    grid[door_pos] = '.'

            grid[graph_pos[graph_idx]] = '.'
            grid[pos] = green('@')
            graph_pos[graph_idx] = pos

            if last_pos and grid[last_pos] != '.':
                grid[last_pos] = '@'
            last_pos = pos

            grid.print()
            input()

    def run(self):
        tic()
        cached_paths = {}
        min_path = self.find_min_path(
            ['@' for _ in self.graphs],
            captured_keys=set(),
            cached_paths=cached_paths,
        )
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

Problem(example1, 1).run() | eq(8)
Problem(example2, 1).run() | eq(86)
Problem(example3, 1).run() | eq(132)
Problem(example4, 1).run() | eq(136)
Problem(example5, 1).run() | eq(81)

input_lines = get_input_lines()
Problem(input_lines, 1).run() | debug('Star 1')

example1 = multiline_lines("""
#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######
""")

example2 = multiline_lines("""
###############
#d.ABC.#.....a#
###############
#######@#######
###############
#b.....#.....c#
###############
""")

example3 = multiline_lines("""
#############
#DcBa.#.GhKl#
#.#######I###
#e#d##@##j#k#
###C#######J#
#fEbA.#.FgHi#
#############
""")

example4 = multiline_lines("""
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

Problem(example1, 2).run() | eq(8)
Problem(example2, 2).run() | eq(24)
Problem(example3, 2).run() | eq(32)
Problem(example4, 7).run() | eq(72)

Problem(input_lines, 2).run() | debug('Star 2')
