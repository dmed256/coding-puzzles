from repo_utils import *

input_lines = get_input_lines()

regex_directions = {
    'W': GRID_LEFT,
    'S': GRID_DOWN,
    'E': GRID_RIGHT,
    'N': GRID_UP,
}

def parse_region(value, ptr):
    children = []
    current_word = []
    while ptr < len(value):
        c = value[ptr]

        if c == '(':
            ptr, node = parse_region(value, ptr + 1)
            current_word.append(node)
            continue

        if c == ')':
            ptr += 1
            break

        elif c == '|':
            children.append(current_word)
            current_word = []
        else:
            if not current_word or type(current_word[-1]) is not str:
                current_word.append('')
            current_word[-1] += c

        ptr += 1

    if current_word:
        children.append(current_word)

    children = [
        child
        for child in children
        if child
    ]

    return ptr, children

def traverse(node, depth, pos, points):
    positions = [pos]
    output = []
    for option in node:
        for value in option:
            if type(value) is str:
                next_positions = [
                    traverse_string(value, pos, points)
                    for pos in positions
                ]
            else:
                next_positions = [
                    new_pos
                    for pos in positions
                    for new_pos in traverse(value, depth + 1, pos, points)
                ]

            positions = next_positions

        output.extend(next_positions)
        positions = [pos]

    return output

def traverse_string(value, pos, points):
    for c in value:
        direction = regex_directions[c]

        pos = apply_direction(pos, direction)
        points.add(pos)

        pos = apply_direction(pos, direction)
        points.add(pos)

    return pos

def run(problem, lines):
    value = lines[0][1:-1]
    _, tree = parse_region(value, 0)

    start_pos = (0, 0)
    points = set([start_pos])
    traverse(tree, 0, start_pos, points)

    grid = Grid.from_points(
        points,
        set_value='.',
        unset_value='#',
    )

    # Points are offset so (0, 0) is at the top-left
    min_x = min(x for x, y in points)
    min_y = min(y for x, y in points)
    start_pos = (-min_x, -min_y)

    grid[start_pos] = 'X'

    queue = [(0, start_pos)]
    room_doors = defaultdict(int)
    visited = {start_pos}
    while queue:
        steps, pos = queue.pop()

        for npos in grid.neighbors(pos):
            if npos in visited:
                continue
            visited.add(npos)

            v = grid[npos]
            if v == '#':
                continue

            npos_steps = steps + 1
            queue.append((npos_steps, npos))

            # Every odd step is a door
            # Every even step is a room
            if npos_steps % 2 == 0:
                room_doors[npos] = npos_steps // 2

    max_room_doors = max(room_doors.values())

    far_rooms = len([
        room
        for room, doors in room_doors.items()
        if 1000 <= doors
    ])

    if problem == 1:
        return max_room_doors

    return far_rooms

example1 = multiline_lines(r"""
^WNE$
""")
run(1, example1) | eq(3)

example2 = multiline_lines(r"""
^ENWWW(NEEE|SSE(EE|N))$
""")
run(1, example2) | eq(10)

example3 = multiline_lines(r"""
^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$
""")
run(1, example3) | eq(18)

example4 = multiline_lines(r"""
^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$
""")
run(1, example4) | eq(23)

example5 = multiline_lines(r"""
^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$
""")
run(1, example5) | eq(31)

run(1, input_lines) | debug('Star 1') | eq(3014)

run(2, input_lines) | debug('Star 2') | eq(8279)
