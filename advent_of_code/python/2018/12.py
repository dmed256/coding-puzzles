from repo_utils import *

input_lines = get_input_lines()

DX = [-2, -1, 0, 1, 2]

def run(problem, lines):
    state = lines[0].split('initial state: ')[1]

    makes_pot = set()
    for line in lines[2:]:
        left, right = line.split(' => ')

        if right != '#':
            continue

        makes_pot.add(sum(
            1 << i if left[i] == '#' else 0
            for i in range(5)
        ))

    nodes = {
        i
        for i, c in enumerate(state)
        if c == '#'
    }

    offset = min(nodes)
    offsets = [offset]
    values = [sorted([x - offset for x in nodes])]

    visited = {
        tuple(values[0]): -1
    }

    generations = 50000000000 if problem == 2 else 20
    for generation in range(generations):
        next_nodes = set()

        possible_x = {
            node_x + dx
            for node_x in nodes
            for dx in DX
        }
        for x in possible_x:
            checksum = sum(
                1 << i if (x + dx) in nodes else 0
                for i, dx in enumerate(DX)
            )
            if checksum in makes_pot:
                next_nodes.add(x)

        nodes = next_nodes

        if problem == 1:
            continue

        offset = min(nodes)
        offsets.append(offset)
        values.append(sorted([x - offset for x in nodes]))

        key = tuple(values[-1])
        if key in visited:
            break
        visited[key] = generation + 1

    if problem == 1:
        return sum(nodes)

    cycle_start = visited[tuple(values[-1])]
    cycle_end = len(values) - 1
    assert cycle_start == cycle_end - 1

    dx = offsets[cycle_end] - offsets[cycle_start]

    base_value = sum(values[cycle_start])

    generations_left = generations - cycle_start
    offset_start = offsets[cycle_start]
    generation_increase = offset_start + (dx * generations_left)

    return base_value + (len(nodes) * generation_increase)

example1 = multiline_lines(r"""
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
""")

run(1, example1) | eq(325)

run(1, input_lines) | debug('Star 1') | eq(3410)

run(2, input_lines) | debug('Star 2') | eq(4000000001480)
