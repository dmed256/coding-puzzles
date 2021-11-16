from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

directions3 = [
    (dx, dy, dz)
    for dx in [-1, 0, 1]
    for dy in [-1, 0, 1]
    for dz in [-1, 0, 1]
    if (dx, dy, dz) != (0, 0, 0)
]

directions4 = [
    (dx, dy, dz, dw)
    for dx in [-1, 0, 1]
    for dy in [-1, 0, 1]
    for dz in [-1, 0, 1]
    for dw in [-1, 0, 1]
    if (dx, dy, dz, dw) != (0, 0, 0, 0)
]

def get_neighbors(pos):
    directions = (
        directions3
        if len(pos) == 3 else
        directions4
    )
    return [
        add_tuples(pos, direction)
        for direction in directions
    ]

def get_active_neigbor_count(nodes, pos):
    return len([
        n
        for n in get_neighbors(pos)
        if n in nodes
    ])

def timestep(nodes):
    next_nodes = set()

    empty_nodes = {
        n
        for node in nodes
        for n in get_neighbors(node)
        if n not in nodes
    }

    for n in nodes:
        count = get_active_neigbor_count(nodes, n)
        if 2 <= count <= 3:
            next_nodes.add(n)

    for n in empty_nodes:
        count = get_active_neigbor_count(nodes, n)
        if count == 3:
            next_nodes.add(n)

    return next_nodes

def run(lines, problem):
    nodes = {
        (x, y, 0)
        for y, line in enumerate(lines)
            for x, v in enumerate(line)
            if v == '#'
    }
    if problem == 2:
        nodes = {
            (*n, 0)
            for n in nodes
        }

    for i in range(6):
        nodes = timestep(nodes)

    return len(nodes)

example1 = multiline_lines(r"""
.#.
..#
###
""")

run(example1, 1) | eq(112)

run(input_lines, 1) | debug('Star 1') | eq(263)

run(example1, 2) | eq(848)

run(input_lines, 2) | debug('Star 2') | eq(1680)
