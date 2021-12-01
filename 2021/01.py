from advent_of_code import *

input_lines = get_input_lines()

def run(lines, window):
    v = [int(x) for x in lines]

    v1 = sum(v[:window])
    count = 0
    for i in range(1, len(v) - window + 1):
        v2 = sum(v[i:i + window])
        if v1 < v2:
            count += 1
        v1 = v2
    return count

example1 = multiline_lines(r"""
199
200
208
210
200
207
240
269
260
263
""")

run(example1, 1) | eq(7)

run(input_lines, 1) | debug('Star 1') | eq(1521)

run(example1, 3) | eq(5)

run(input_lines, 3) | debug('Star 2') | eq(1543)
