from repo_utils import *

input_lines = get_input_lines()

def parse_lines(lines):
    nodes = {}
    for line in lines[2:]:
        node, size, used, _avail, _perc = [x.strip() for x in line.split()]

        x, y = node.replace('/dev/grid/node-x', '').split('-y')
        x = int(x)
        y = int(y)

        size = int(size[:-1])
        used = int(used[:-1])

        nodes[(x, y)] = (used, size)

    return nodes

def run(lines):
    nodes = parse_lines(lines)

    infos = list(nodes.values())
    pairs = 0
    for i in range(len(infos)):
        used1, size1 = infos[i]
        avail1 = size1 - used1
        for j in range(i + 1, len(infos)):
            used2, size2 = infos[j]
            avail2 = size2 - used2
            if used1 and used1 < avail2:
                pairs += 1
            if used2 and used2 < avail1:
                pairs += 1

    return pairs

def run2(lines):
    nodes = parse_lines(lines)

    grid = Grid.from_points(nodes.keys())
    for pos, info in nodes.items():
        grid[pos] = info

    pos  = (grid.width - 1, 0)
    goal = (0, 0)

    # TODO: ???

run(input_lines) | debug('Star 1') | eq(1045)

# run2(input_lines) | submit(2)
