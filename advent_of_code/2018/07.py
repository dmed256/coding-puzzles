from repo_utils import *

input_lines = get_input_lines()

def parse_lines(lines):
    dependencies = defaultdict(set)
    unblocks = defaultdict(set)
    nodes = set()
    for line in lines:
        parts = line.split()
        dep = parts[1]
        node = parts[7]

        dependencies[node].add(dep)
        unblocks[dep].add(node)
        nodes |= {dep, node}

    starting_nodes = [
        node
        for node in nodes
        if node not in dependencies
    ]

    return starting_nodes, dependencies, unblocks

def run(lines):
    starting_nodes, dependencies, unblocks = parse_lines(lines)

    queue = starting_nodes
    heapq.heapify(queue)

    ans = ''
    while queue:
        node = heapq.heappop(queue)
        ans += node

        next_nodes = []
        for enabled_node in unblocks[node]:
            dependencies[enabled_node] -= {node}
            if not dependencies[enabled_node]:
                next_nodes.append(enabled_node)

        for next_node in sorted(next_nodes):
            heapq.heappush(queue, next_node)

    return ans

def run2(lines, elves, base_cost):
    starting_nodes, dependencies, unblocks = parse_lines(lines)

    pass


example1 = multiline_lines(r"""
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
""")

run(example1) | eq('CABDFE')

run(input_lines) | debug('Star 1') | eq('CGKMUWXFAIHSYDNLJQTREOPZBV')

# run2(example1, 2, 0) | eq(15)

# run2(input_lines, 5, 60) | submit(2)
