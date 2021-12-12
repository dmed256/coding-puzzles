from repo_utils import *

input_lines = get_input_lines()

def run(problem, lines):
    connections = defaultdict(list)
    for line in lines:
        left, right = line.split('-')
        connections[left].append(right)
        connections[right].append(left)

    small_caves = [
        conn
        for conn in connections.keys()
        if conn == conn.lower()
    ]
    large_caves = {
        conn
        for conn in connections.keys()
        if conn == conn.upper()
    }

    extra_small_cave = None if problem == 2 else 'hi'

    queue = [('start', small_caves, extra_small_cave)]
    paths = 0
    while queue:
        node, small_caves, extra_small_cave = queue.pop(0)

        for next_node in connections[node]:
            if next_node == 'start':
                continue

            if next_node == 'end':
                paths += 1
                continue

            if next_node in large_caves:
                queue.append((next_node, small_caves, extra_small_cave))
                continue

            if next_node not in small_caves:
                if extra_small_cave is None:
                    queue.append((next_node, small_caves, next_node))
                continue

            next_small_caves = deepcopy(small_caves)
            next_small_caves.pop(small_caves.index(next_node))
            queue.append((next_node, next_small_caves, extra_small_cave))

    return paths

example1 = multiline_lines(r"""
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
""")

run(1, example1) | eq(226)

run(1, input_lines) | debug('Star 1') | eq(3856)

run(2, example1) | eq(3509)

run(2, input_lines) | debug('Star 2') | eq(116692)
