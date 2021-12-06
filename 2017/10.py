from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

def hash_values(values, lengths, rounds):
    values = deepcopy(values)

    ptr = 0
    skip = -1
    for _ in range(rounds):
        for length in lengths:
            skip += 1

            if length > len(values):
                continue

            p1 = ptr
            p2 = (ptr + length) % len(values)

            ptr = (ptr + length + skip) % len(values)

            if p1 < p2:
                values[p1:p2] = reversed(values[p1:p2])
            elif length:
                start = values[:p2]
                end = values[p1:]
                chunk = (end + start)[::-1]
                values[:p2] = chunk[len(end):]
                values[p1:] = chunk[:len(end)]

    return values

def run(lines, chars):
    values = list(range(chars))
    lengths = [int(x) for x in lines[0].split(',')]

    values = hash_values(values, lengths, 1)
    return values[0] * values[1]

def run2(content):
    if type(content) is list:
        content = content[0]

    values = list(range(256))
    lengths = (
        [ord(c) for c in content]
        + [17, 31, 73, 47, 23]
    )

    values = hash_values(values, lengths, 64)

    hashed_value = []
    for i in range(0, 256, 16):
        value = 0
        for j in range(i, i + 16):
            value ^= values[j]
        hashed_value.append(value)

    def hex_value(v):
        h = hex(v)[2:]
        if len(h) == 2:
            return h
        return '0' + h

    return ''.join(
        hex_value(c)
        for c in hashed_value
    )

example1 = multiline_lines(r"""
3,4,1,5
""")

run(example1, 5) | eq(12)

run(input_lines, 256) | debug('Star 1') | eq(8536)

run2('') | eq('a2582a3a0e66e6e86e3812dcb672a272')
run2('AoC 2017') | eq('33efeb34ea91902bb2f59c9920caa6cd')
run2('1,2,3') | eq('3efbe78a8d82f29979031a4aa0b16a9d')
run2('1,2,4') | eq('63960835bcdc130f0b66d7ff4f6a5a8e')

run2(input_lines) | debug('Star 2') | eq('aff593797989d665349efe11bb4fd99b')
