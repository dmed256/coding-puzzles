from advent_of_code import *

input_lines = get_input_lines()

def run(lines, preamble):
    values = [int(i) for i in lines]

    sums = {}
    for i in range(preamble):
        vi = values[i]
        for j in range(i + 1, preamble):
            sum_value = vi + values[j]
            sums[sum_value] = sums.get(sum_value, 0) + 1

    for i in range(preamble, len(values)):
        vi = values[i]
        if vi not in sums:
            return vi

        removed_index = i - preamble
        removed_value = values[removed_index]
        for j in range(removed_index + 1, removed_index + preamble):
            removed_sum = removed_value + values[j]
            if sums[removed_sum] > 1:
                sums[removed_sum] -= 1
            else:
                del sums[removed_sum]

        for j in range(i - preamble, i):
            sum_value = values[j] + vi
            sums[sum_value] = sums.get(sum_value, 0) + 1

example1 = [
    str(i)
    for i in (list(range(1, 26)) + [100])
]

example2 = multiline_lines(r"""
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
""")

run(example1, 25) | eq(100)
run(example2, 5) | eq(127)

run(input_lines, 25) | debug('Star 1') | eq(21806024)

def run2(lines, preamble):
    values = [int(i) for i in lines]
    result = run(lines, preamble)

    for i in range(len(values)):
        summed_value = 0
        for j in range(i, len(values)):
            summed_value += values[j]
            if summed_value > result:
                break
            elif summed_value == result:
                continuous_values = values[i:j + 1]
                return min(continuous_values) + max(continuous_values)

run2(example2, 5) | eq(62)

run2(input_lines, 25) | debug('Star 2') | eq(2986195)
