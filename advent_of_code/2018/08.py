from repo_utils import *


input_lines = get_input_lines()

Node = namedtuple('Node', ['id', 'children', 'metadata'])


def parse_tree(ptr, node_id, values):
    child_count, metadata_count = values[ptr:ptr + 2]
    ptr += 2

    children = []
    for _ in range(child_count):
        ptr, node_id, child = parse_tree(ptr, node_id, values)
        children.append(child)

    metadata = values[ptr:ptr + metadata_count]
    ptr += metadata_count

    return ptr, node_id + 1, Node(node_id, children, metadata)


def node_value(problem, node, cache):
    if node.id in cache:
        return cache[node.id]

    if problem == 1:
        value = sum(
            node_value(problem, child, cache)
            for child in node.children
        ) + sum(node.metadata)
    elif not node.children:
        value = sum(node.metadata)
    else:
        value = sum(
            node_value(problem, node.children[child_idx - 1], cache)
            for child_idx in node.metadata
            if 0 <= (child_idx - 1) < len(node.children)
        )

    cache[node.id] = value
    return value


def run(problem, lines):
    values = [int(c) for c in lines[0].split()]

    _, _, root = parse_tree(0, 0, values)

    return node_value(problem, root, {})

example1 = multiline_lines(r"""
2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
""")

run(1, example1) | eq(138)

run(1, input_lines) | debug('Star 1') | eq(42472)

run(2, example1) | eq(66)

run(2, input_lines) | debug('Star 2') | eq(21810)
