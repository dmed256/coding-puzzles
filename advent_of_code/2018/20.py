from repo_utils import *

input_lines = get_input_lines()

Node = namedtuple('Node', [
    'children',
    'concat_values',
])

regex_directions = {
    'W': GRID_LEFT,
    'S': GRID_DOWN,
    'E': GRID_RIGHT,
    'N': GRID_UP,
}

def parse_region(value, ptr):
    children = ['']
    concat_values = True

    while ptr < len(value):
        c = value[ptr]

        if c == '(':
            ptr, node = parse_region(value, ptr + 1)
            children.append(node)
            continue

        if c == ')':
            ptr += 1
            break

        elif c == '|':
            concat_values = False
            children.append('')
        else:
            children[-1] += c

        ptr += 1

    children = [
        child
        for child in children
        if child
    ]

    return ptr, Node(
        children=children,
        concat_values=concat_values,
    )

def traverse(node, depth, pos, points):
    positions = [pos]
    output = []
    for child in node.children:
        if type(child) is str:
            next_positions = [
                traverse_string(child, pos, points)
                for pos in positions
            ]
        else:
            next_positions = [
                new_pos
                for pos in positions
                for new_pos in traverse(child, depth + 1, pos, points)
            ]

        if node.concat_values:
            positions = next_positions
        else:
            output.extend(next_positions)
            positions = [pos]

    if node.concat_values:
        return positions

    return output

def traverse_string(value, pos, points):
    for c in value:
        direction = regex_directions[c]

        pos = apply_direction(pos, direction)
        points.add(pos)
        print(pos)

        pos = apply_direction(pos, direction)
        points.add(pos)
        print(pos)

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

    print(value)
    print(tree)
    grid.print()

    return None

example1 = multiline_lines(r"""
^WNE$
""")
run(1, example1) | eq(3)

example2 = multiline_lines(r"""
^ENWWW(NEEE|SSE(EE|N))$
""")
run(1, example2) | eq(10)
raise 1

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

run(1, input_lines) | submit(1)

# run(2, example1) | eq()

# run(2, input_lines) | submit(2)
