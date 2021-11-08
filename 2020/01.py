from advent_of_code import *

def run(lines):
    values = [int(line) for line in lines]
    for i in range(len(values)):
        v1 = values[i]
        for j in range(i + 1, len(values)):
            v2= values[j]
            if v1 + v2 == 2020:
                return v1 * v2

example1 = multiline_lines(r"""
1721
979
366
299
675
1456
""")

run(example1) | eq(514579)

input_lines = get_input_lines()

run(input_lines) | debug('Star 1')

def run2(lines):
    values = [int(line) for line in lines]
    for i in range(len(values)):
        v1 = values[i]
        for j in range(i + 1, len(values)):
            v2= values[j]
            for k in range(j + 1, len(values)):
                v3 = values[k]
                if v1 + v2 + v3 == 2020:
                    return v1 * v2 * v3

run2(example1) | eq(241861950)
run2(input_lines) | debug('Star 2')
