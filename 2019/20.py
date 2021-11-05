from advent_of_code import *

class Problem:
    def __init__(self, lines, problem):
        self.setup_grid(lines)
        self.setup_graph()

        self.start_pos = self.teleporters['A'][0]
        self.end_pos = self.teleporters['Z'][0]

        self.using_depth = problem == 2

    @staticmethod
    def get_graph_type(value):
        if value in ['#', ' ']:
            return Graph.Type.WALL
        if value == '.':
            return Graph.Type.NOTHING
        return Graph.Type.OBJECT

    def setup_grid(self, lines):
        self.grid = Grid(lines, default_value=' ')

        teleporter_positions = {}
        self.teleporter_goes_up = {}
        for (x1, y1, v1) in self.grid:
            if not v1.isupper():
                continue

            p1 = (x1, y1)
            [p2, v2, prev_node1] = self.get_teleporter_info(p1)
            [_, _, prev_node2] = self.get_teleporter_info(p2)


            if prev_node1:
                pos = (prev_node1, p1, p2)
            else:
                pos = (prev_node2, p2, p1)

            (prev_node, p1, p2) = pos
            for direction in DIRECTIONS:
                if apply_direction(p1, direction) == direction:
                    break

            (x2, y2) = p2
            goes_up = (
                (x2 < 1 or (self.grid.width - 2) < x2) or
                (y2 < 1 or (self.grid.height - 2) < y2)
            )

            name = {
                UP: v1 + v2,
                DOWN: v2 + v1,
                LEFT: v1 + v2,
                RIGHT: v2 + v1,
            }[direction]

            teleporter_positions[pos] = name
            self.teleporter_goes_up[prev_node] = goes_up

        bitly = {
            'AA': 'A',
            'ZZ': 'Z',
        }
        letter = 'a'
        for name in teleporter_positions.values():
            if name not in bitly:
                bitly[name] = letter
                letter = chr(ord(letter) + 1)

        self.teleporters = {}
        for (prev_node, p1, p2), name in teleporter_positions.items():
            name = bitly[name]
            self.teleporters[name] = self.teleporters.get(name, []) + [prev_node]

        for (prev_node, p1, p2), name in teleporter_positions.items():
            self.grid[p1] = bitly[name]
            self.grid[p2] = ' '

    def get_teleporter_info(self, p1):
        p2 = None
        v2 = None
        prev_node = None

        for neighbor in self.grid.neighbors(p1):
            maybe_v2 = self.grid[neighbor]
            if maybe_v2.isupper():
                p2 = neighbor
                v2 = maybe_v2
            elif maybe_v2 == '.':
                prev_node = neighbor

        return [p2, v2, prev_node]

    def setup_graph(self):
        doors = [
            p
            for positions in self.teleporters.values()
            for p in positions
        ]

        graph = Graph(
            self.grid,
            start_pos=doors,
            get_type=Problem.get_graph_type,
        )

        self.paths = {
            p: graph.find_paths(p, doors)
            for p in doors
        }

        self.use_teleporter = {}
        for positions in self.teleporters.values():
            if len(positions) == 2:
                [p1, p2] = positions
                self.use_teleporter[p1] = p2
                self.use_teleporter[p2] = p1

    @staticmethod
    def position_cost(position):
        [(pos, depth), path, *other] = position

        depth_cost = max(1, (depth - 20))

        return len(path) * depth_cost

    def trim_positions(self, positions, new_positions, min_pos_path_length, min_path):
        if self.using_depth:
            min_zpositions = [
                [zpos, path, *other]
                for [zpos, path, *other] in new_positions
                if zpos not in min_pos_path_length
                or len(path) < min_pos_path_length[zpos]
            ]
            for [zpos, path, *other] in min_zpositions:
                min_pos_path_length[zpos] = len(path)
            updated_zpos = set([
                zpos
                for [zpos, *other] in min_zpositions
            ])
            positions = [
                [zpos, *other]
                for [zpos, *other] in positions
                if zpos not in updated_zpos
            ] + min_zpositions
        else:
            min_positions = [
                [(pos, depth), path, *other]
                for [(pos, depth), path, *other] in new_positions
                if pos not in min_pos_path_length
                or len(path) < min_pos_path_length[pos]
            ]
            for [(pos, depth), path, *other] in min_positions:
                min_pos_path_length[pos] = len(path)
            updated_pos = set([
                pos
                for [(pos, depth), *other] in min_positions
            ])
            positions = [
                [(pos, depth), *other]
                for [(pos, depth), *other] in positions
                if pos not in updated_pos
            ] + min_positions

        positions.sort(key=Problem.position_cost)
        return positions

    def find_min_path(self, positions):
        [(pos, depth), prev_path, explored_doors] = positions.pop(0)

        min_path = None
        new_positions = []
        for path in self.paths[pos]:
            target = path[-1]
            ztarget = (target, depth)

            if target in explored_doors or ztarget in explored_doors:
                continue

            path = [*prev_path, *[(p, depth) for p in path]]

            depth2 = (
                depth - 1
                if self.teleporter_goes_up[target] else
                depth + 1
            )
            if depth2 > 1000:
                continue

            if target == self.end_pos and (depth == 0 or not self.using_depth):
                min_path = shortest_list([
                    min_path,
                    path,
                ])
                continue

            # Doors are closed
            if self.using_depth and depth > 0 and target == self.end_pos:
                continue
            if target == self.start_pos:
                continue
            if self.using_depth and depth2 < 0:
                continue

            target2 = self.use_teleporter[target]
            ztarget2 = (target2, depth2)
            if self.using_depth:
                new_explored_doors = set([ztarget, ztarget2])
            else:
                new_explored_doors = set([target, target2])

            new_positions.append([
                ztarget2,
                [*path, ztarget2],
                explored_doors | new_explored_doors,
            ])

        return [new_positions, min_path]

    def print_path(self, path):
        if path is None:
            return

        prev_depth = 0
        for ((x, y), depth) in path:
            if self.using_depth and depth != prev_depth:
                print(yellow(f'{prev_depth} -> {depth}'))
                prev_depth = depth
            print((x, y, depth))


    def run(self):
        self.grid.print()

        init_pos = (self.start_pos, 0)

        min_path = None
        positions = [[init_pos, [], set()]]
        min_pos_path_length = {}
        while positions:
            [new_positions, min_path2] = self.find_min_path(positions)
            min_path = shortest_list([min_path, min_path2])
            positions = self.trim_positions(
                positions,
                new_positions,
                min_pos_path_length,
                min_path,
            )

        # self.print_path(min_path)

        return len(min_path)

example1 = multiline_lines("""
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
""", strip_lines=False)

example2 = multiline_lines("""
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
""", strip_lines=False)

Problem(example1, 1).run() | eq(23)
Problem(example2, 1).run() | eq(58)

input_lines = get_input_lines()
Problem(input_lines, 1).run() | debug('Star 1')

example1 = multiline_lines("""
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
""", strip_lines=False)

Problem(example1, 2).run() | eq(396)
Problem(input_lines, 2).run() | debug('Star 2')
