from repo_utils import *

input_lines = get_input_lines()

def parse_lines(problem, lines):
    if problem == 1:
        applied_values = [1, None, 0]
    else:
        applied_values = [1, 2, -1]

    for line in lines:
        words = line.split(' ')
        min_x, min_y = words[-3].split(',')
        min_x, min_y = int(min_x), int(min_y)

        max_x, max_y = words[-1].split(',')
        max_x, max_y = int(max_x), int(max_y)

        if line.startswith('turn on '):
            value_idx = 0
        elif line.startswith('toggle '):
            value_idx = 1
        elif line.startswith('turn off '):
            value_idx = 2

        value = applied_values[value_idx]

        yield (
            (min_x, max_x),
            (min_y, max_y),
            value,
        )

def run(lines):
    l = [0 for i in range(1000 * 1000)]

    for (min_x, max_x), (min_y, max_y), value in parse_lines(1, lines):
        if value is not None:
            for y in range(min_y, max_y + 1):
                for x in range(min_x, max_x + 1):
                    l[x + 1000*y] = value
        else:
            for y in range(min_y, max_y + 1):
                for x in range(min_x, max_x + 1):
                    l[x + 1000*y] = (l[x + 1000*y] + 1) % 2

    return sum(l)


def run2(lines):
    l = [0 for i in range(1000 * 1000)]

    for (min_x, max_x), (min_y, max_y), value in parse_lines(2, lines):
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                l[x + 1000*y] = max(0, l[x + 1000*y] + value)

    return sum(l)

run(['turn on 0,0 through 999,999']) | eq(1000 * 1000)
run(['toggle 0,0 through 999,0']) | eq(1000)
run(['turn off 499,499 through 500,500']) | eq(0)

run(input_lines) | debug('Star 1')

run2(['turn on 0,0 through 0,0']) | eq(1)
run2(['toggle 0,0 through 999,999']) | eq(2000000)

run2(input_lines) | debug('Star 2')
