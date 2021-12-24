from repo_utils import *

input_value = get_input()
input_lines = get_input_lines()

def run(problem, lines):
    matches = defaultdict(set)
    for line in lines:
        a, b = line.split('/')
        a = int(a)
        b = int(b)

        matches[a].add((a, b))
        matches[b].add((a, b))

    if problem == 1:
        init_value = 0
    else:
        init_value = (0, 0)

    q = [(0, set(), init_value)]
    max_value = init_value
    while q:
        end, pins, value = q.pop(0)
        max_value = max(max_value, value)
        for pin in matches[end] - pins:
            next_end = sum(pin) - end

            if problem == 1:
                pin_value = value + end + next_end
            else:
                pin_value = (value[0] + 1, value[1] + end + next_end)

            q.append((next_end, pins | {pin}, pin_value))

    if problem == 1:
        return max_value
    else:
        return max_value[1]

example1 = multiline_lines(r"""
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10
""")

run(1, example1) | eq(31)

run(1, input_lines) | debug('Star 1') | eq(1695)

run(2, example1) | eq(19)

run(2, input_lines) | debug('Star 2') | eq(1673)
