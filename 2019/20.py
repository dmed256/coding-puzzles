from advent_of_code import *

def setup_grid(lines):
    grid = Grid(lines, default_value=' ')

    teleporter_positions = {}
    for (x1, y1, v1) in grid:
        if not v1.isupper():
            continue

        p1 = (x1, y1)
        [p2, v2, prev_node1] = get_teleporter_info(grid, p1)
        [_, _, prev_node2] = get_teleporter_info(grid, p2)


        if prev_node1:
            pos = (prev_node1, p1, p2)
        else:
            pos = (prev_node2, p2, p1)

        (prev_node, p1, p2) = pos
        for direction in DIRECTIONS:
            if apply_direction(p1, direction) == direction:
                break

        name = {
            UP: v1 + v2,
            DOWN: v2 + v1,
            LEFT: v1 + v2,
            RIGHT: v2 + v1,
        }[direction]

        teleporter_positions[pos] = name

    bitly = {
        'AA': 'A',
        'ZZ': 'Z',
    }
    letter = 'a'
    for name in teleporter_positions.values():
        if name not in bitly:
            bitly[name] = letter
            letter = chr(ord(letter) + 1)

    teleporters = {}
    for (prev_node, p1, p2), name in teleporter_positions.items():
        name = bitly[name]
        teleporters[name] = teleporters.get(name, []) + [prev_node]

    for (prev_node, p1, p2), name in teleporter_positions.items():
        grid[p1] = bitly[name]
        grid[p2] = ' '

    return [grid, teleporters]

def get_teleporter_info(grid, p1):
    p2 = None
    v2 = None
    prev_node = None

    for neighbor in grid.neighbors(p1):
        maybe_v2 = grid[neighbor]
        if maybe_v2.isupper():
            p2 = neighbor
            v2 = maybe_v2
        elif maybe_v2 == '.':
            prev_node = neighbor

    return [p2, v2, prev_node]

def get_graph_type(value):
    if value in ['#', ' ']:
        return Graph.Type.WALL
    if value == '.':
        return Graph.Type.NOTHING
    return Graph.Type.OBJECT

def run(lines):
    [grid, teleporters] = setup_grid(lines)
    grid.print()

    start_pos = teleporters['A'][0]
    end_pos = teleporters['Z'][0]
    doors = [
        p
        for positions in teleporters.values()
        for p in positions
    ]
    use_teleporter = {}
    for positions in teleporters.values():
        if len(positions) == 2:
            [p1, p2] = positions
            use_teleporter[p1] = p2
            use_teleporter[p2] = p1

    graph = Graph(
        grid,
        start_pos=doors,
        get_type=get_graph_type,
    )
    paths = {
        p: graph.find_paths(p, doors)
        for p in doors
    }

    cache = {}
    def find_min_path(pos, explored_doors):
        min_path = None
        for path in paths[pos]:
            target = path[-1]
            if target in explored_doors:
                continue

            if target == end_pos:
                next_path = []
            elif target in cache:
                next_path = cache[target]
            else:
                target2 = use_teleporter[target]
                next_path = find_min_path(
                    target2,
                    explored_doors | set([target, target2])
                )
                if next_path is not None:
                    next_path.insert(0, 'T')
                cache[target] = next_path

            if next_path is None:
                continue

            next_path = [*path, *next_path]
            min_path = shortest_list([min_path, next_path])

        return min_path

    min_path = find_min_path(start_pos, set([start_pos]))
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

run(example1) | eq(23)
run(example2) | eq(58)

input_lines = get_input_lines()
run(input_lines) | debug('Star 1')