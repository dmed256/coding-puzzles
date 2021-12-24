from repo_utils import *

input_lines = get_input_lines()

def run(problem, lines):
    freq = 0
    seen = set()

    while True:
        for line in lines:
            sign, value = line[0], int(line[1:])
            if sign == '-':
                value = -value

            freq += value
            if problem == 2 and freq in seen:
                return freq

            seen.add(freq)

        if problem == 1:
            break

    return freq

example1 = multiline_lines(r"""
-1
-2
-3
""")

run(1, example1) | eq(-6)

run(1, input_lines) | debug('Star 1') | eq(518)

run(2, input_lines) | debug('Star 2') | eq(72889)
