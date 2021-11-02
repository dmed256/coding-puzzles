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
    outputs = pmap('fft', apply_blocked_fft, [value, digits])
    output = np.sum(outputs, axis=0).astype(int)

    # Get the first digit only
    for i in range(digits):
        output[i] = abs(output[i]) % 10

    return output

def apply_fast_fft(value, digits):




def get_subdigit(value, offset, count):
    subdigit = 0
    for i in range(offset, offset + count):
        subdigit *= 10
        subdigit += value[i]
    return subdigit

def run(value, problem):
    value = [int(c) for c in value]
    if problem == 2:
        value = value * 10000
    digits = len(value)

    for i in range(100):
        if problem == 2:
            tic()

        value = apply_fft(value, digits)

        if problem == 2:
            toc(f'FFT phase = {i}')

    if problem == 1:
        return get_subdigit(value, 0, 8)

    offset = get_subdigit(value, 0, 7)
    return get_subdigit(value, offset, 8)

example1 = '80871224585914546619083218645595'
example2 = '19617804207202209144916044189917'
example3 = '69317163492948606335995924319873'

run(example1, 1) | eq(24176176)
run(example2, 1) | eq(73745418)
run(example3, 1) | eq(52432133)

input_value = get_input()

run(input_value, 1) | debug('Star 1')

example1 = '03036732577212944063491565474664'
example2 = '02935109699940807407585447034323'
example3 = '03081770884921959731165446850517'

print('example1')
run(example1, 2) | eq(84462026)
# print('example2')
# run(example2, 2) | eq(78725270)
# print('example3')
# run(example3, 2) | eq(53553731)

# run(input_value, 2) | debug('Star 2')
