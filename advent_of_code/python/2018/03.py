from repo_utils import *

input_lines = get_input_lines()

def run(problem, lines):
    points = defaultdict(int)

    claims = []
    for line in lines:
        idx, pos, rect = (
            line
            .replace('#', '')
            .replace('@ ', '')
            .replace(':', '')
            .split()
        )
        idx = int(idx)
        x0, y0 = [int(x) for x in pos.split(',')]
        rx, ry = [int(x) for x in rect.split('x')]

        claims.append((idx, (x0, y0), (rx, ry)))

    for idx, (x0, y0), (rx, ry) in claims:
        for y in range(y0, y0 + ry):
            for x in range(x0, x0 + rx):
                points[(x, y)] += 1

    if problem == 1:
        return len([
            1
            for count in points.values()
            if count >= 2
        ])

    for idx, (x0, y0), (rx, ry) in claims:
        found = all(
            points[(x, y)] == 1
            for x in range(x0, x0 + rx)
            for y in range(y0, y0 + ry)
        )
        if found:
            return idx

run(1, input_lines) | debug('Star 1') | eq(101781)

run(2, input_lines) | debug('Star 2') | eq(909)
