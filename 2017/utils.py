from advent_of_code import *

def knot_hash_values(values, lengths, rounds):
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

def get_knot_hash(content):
    if type(content) is list:
        content = content[0]

    values = list(range(256))
    lengths = (
        [ord(c) for c in content]
        + [17, 31, 73, 47, 23]
    )

    values = knot_hash_values(values, lengths, 64)

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
