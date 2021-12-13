from repo_utils import *

input_lines = get_input_lines()

def run(problem, lines):
    nodes = {}
    for line in lines[2:]:
        node, size, used, avail, _perc = [x.strip() for x in line.split()]

        x, y = node.replace('/dev/grid/node-x', '').split('-y')
        x = int(x)
        y = int(y)

        size = int(size[:-1])
        used = int(used[:-1])
        avail = int(avail[:-1])

        nodes[(x, y)] = (size, used, avail)

    min_x = min([x for x, y in nodes.keys()])
    max_x = max([x for x, y in nodes.keys()])
    min_y = min([y for x, y in nodes.keys()])
    max_y = max([y for x, y in nodes.keys()])

    grid = Grid([
        [None for x in range(min_x, max_x + 1)]
        for y in range(min_y, max_y + 1)
    ])

    for pos, info in nodes.items():
        grid[pos] = info

    infos = list(nodes.values())
    pairs = 0
    for i in range(len(infos)):
        _, used1, avail1 = infos[i]
        for j in range(i + 1, len(infos)):
            _, used2, avail2 = infos[j]
            if used1 and used1 < avail2:
                pairs += 1
            if used2 and used2 < avail1:
                pairs += 1

    return pairs

run(1, input_lines) | debug('Star 1') | eq(1045)

# run(2, example1) | eq()

# run(2, input_lines) | submit(2)
