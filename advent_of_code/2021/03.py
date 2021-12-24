from repo_utils import *

input_value = get_input()
input_lines = get_input_lines()

def get_max_bits(values, bit):
    mask = (1 << bit)
    ones = 0
    for v in values:
        ones += bool(v & mask)

    zeroes = len(values) - ones
    if zeroes < ones:
        return [1]
    if zeroes > ones:
        return [0]
    return [0, 1]

def run(lines):
    bits = len(lines[0])
    values = [
        int(line, 2)
        for line in lines
    ]
    gamma = 0
    epsilon = 0
    for bit in range(bits):
        max_bits = get_max_bits(values, bit)
        if max_bits == [0]:
            gamma += 1 << bit
        else:
            epsilon += 1 << bit

    return gamma * epsilon

example1 = multiline_lines(r"""
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
""")

run(example1) | eq(198)

run(input_lines) | debug('Star 1') | eq(4147524)

def run2(lines):
    bits = len(lines[0])
    original_values = [
        int(line, 2)
        for line in lines
    ]

    oxygen_values = original_values
    co2_values = original_values
    for bit in invrange(bits):
        mask = 1 << bit

        if len(oxygen_values) > 1:
            oxygen_matches = 1 in get_max_bits(oxygen_values, bit)
            oxygen_values = [
                v
                for v in oxygen_values
                if bool(v & mask) == oxygen_matches
            ]

        if len(co2_values) > 1:
            co2_matches = 1 not in get_max_bits(co2_values, bit)
            co2_values = [
                v
                for v in co2_values
                if bool(v & mask) == co2_matches
            ]

    return oxygen_values[0] * co2_values[0]

run2(example1) | eq(230)

run2(input_lines) | debug('Star 2') | eq(3570354)
