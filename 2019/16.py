import numpy as np
import math
from advent_of_code import *

#  I  . -1  .  1  . -1  .  1  . -1  .  1  . -1  .  1  . -1  .  1  . -1  .  1
#  .  I  1  .  . -1 -1  .  .  1  1  .  . -1 -1  .  .  1  1  .  . -1 -1  .  .
#  .  .  I  1  1  .  .  . -1 -1 -1  .  .  .  1  1  1  .  .  . -1 -1 -1  .  .
#  .  .  .  I  1  1  1  .  .  .  . -1 -1 -1 -1  .  .  .  .  1  1  1  1  .  .
#  .  .  .  .  I  1  1  1  1  .  .  .  .  . -1 -1 -1 -1 -1  .  .  .  .  .  1
#  .  .  .  .  .  I  1  1  1  1  1  .  .  .  .  .  . -1 -1 -1 -1 -1 -1  .  .
#  .  .  .  .  .  .  I  1  1  1  1  1  1  .  .  .  .  .  .  . -1 -1 -1 -1 -1
#  .  .  .  .  .  .  .  I  1  1  1  1  1  1  1  .  .  .  .  .  .  .  . -1 -1
#  .  .  .  .  .  .  .  .  I  1  1  1  1  1  1  1  1  .  .  .  .  .  .  .  .
#  .  .  .  .  .  .  .  .  .  I  1  1  1  1  1  1  1  1  1  .  .  .  .  .  .
#  .  .  .  .  .  .  .  .  .  .  I  1  1  1  1  1  1  1  1  1  1  .  .  .  .
#  .  .  .  .  .  .  .  .  .  .  .  I  1  1  1  1  1  1  1  1  1  1  1  .  .
#  .  .  .  .  .  .  .  .  .  .  .  .  I  1  1  1  1  1  1  1  1  1  1  1  1
#  .  .  .  .  .  .  .  .  .  .  .  .  .  I  1  1  1  1  1  1  1  1  1  1  1
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  I  1  1  1  1  1  1  1  1  1  1
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  I  1  1  1  1  1  1  1  1  1
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  I  1  1  1  1  1  1  1  1
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  I  1  1  1  1  1  1  1
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  I  1  1  1  1  1  1
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  I  1  1  1  1  1
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  I  1  1  1  1
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  I  1  1  1
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  I  1  1
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  I  1
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  I

def apply_diagonal(value, output, digits, row0_index, shift, coeff):
    idx_start = row0_index
    idx_end   = idx_start + 1

    output_idx = 0
    output_acc = coeff * value[row0_index]
    while idx_start < digits:
        next_idx_start = min(idx_start + shift, digits)
        # Each row has 1 more entry than the last
        next_idx_end   = min(idx_end + shift + 1, digits)

        output[output_idx] += output_acc

        old = sum(
            value[i]
            for i in range(idx_start, min(idx_end, next_idx_start))
        )
        new = sum(
            value[i]
            for i in range(max(idx_end, next_idx_start), next_idx_end)
        )
        output_acc += coeff * (new - old)

        idx_start = next_idx_start
        idx_end   = next_idx_end
        output_idx += 1


def apply_blocked_fft(blocks, block, value, digits):
    output = np.zeros(digits).astype(int)

    # Apply staggered diagonals
    for row0_index in range(2*block, digits, 2*blocks):
        coeff = 1 if row0_index % 4 else -1
        shift = row0_index + 1
        apply_diagonal(value, output, digits, row0_index, shift, coeff)

    return output

def apply_fft(value, digits):
    if True:
        output = apply_blocked_fft(1, 0, value, digits)
    else:
        outputs = pmap('fft', apply_blocked_fft, [value, digits])
        output = np.sum(outputs, axis=0).astype(int)

    # Get the first digit only
    for i in range(digits):
        output[i] = abs(output[i]) % 10

    return output

def get_subdigit(value, offset, count):
    subdigit = 0
    for i in range(offset, offset + count):
        subdigit *= 10
        subdigit += value[i]
    return subdigit

def run(value):
    value = [int(c) for c in value]
    digits = len(value)

    for i in range(100):
        value = apply_fft(value, digits)

    return get_subdigit(value, 0, 8)

example1 = '80871224585914546619083218645595'
example2 = '19617804207202209144916044189917'
example3 = '69317163492948606335995924319873'

run(example1) | eq(24176176)
run(example2) | eq(73745418)
run(example3) | eq(52432133)

input_value = get_input()

run(input_value) | debug('Star 1') | eq(36627552)

def run2(value):
    value = [int(c) for c in value]
    offset = get_subdigit(value, 0, 7)

    value = value * 10000
    value = value[offset:]
    digits = len(value)

    # Apply top-right 1 matrix
    #
    # 1 1 1 1 1     v1
    # . 1 1 1 1     v2
    # . . 1 1 1  x  v3
    # . . . 1 1     v4
    # . . . . 1     v5

    for loop in range(100):
        last_value = value[-1]
        for i in range(digits - 2, -1, -1):
            last_value = (last_value + value[i]) % 10
            value[i] = last_value

    return get_subdigit(value, 0, 8)

run2(input_value) | debug('Star 2') | eq(79723033)
