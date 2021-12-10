from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

def run(problem, lines):
    tuples = set()
    for line in lines:
        a_, b_ = line.split('/')
        a_ = int(a_)
        b_ = int(b_)
        a = min(a_, b_)
        b = max(a_, b_)

        tuples.add((a, b))

    if problem == 1:
        init_value = 0
    else:
        init_value = (0, 0)

    q = [(0, tuples, init_value)]
    max_value = init_value
    while q:
        end, tuples, value = q.pop(0)
        max_value = max(max_value, value)
        for pin in tuples:
            if problem == 1:
                pin_value = value + sum(pin)
            else:
                pin_value = (value[0] + 1, value[1] + sum(pin))

            if end == pin[0]:
                q.append((pin[1], tuples - {pin}, pin_value))
            elif end == pin[1]:
                q.append((pin[0], tuples - {pin}, pin_value))

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
