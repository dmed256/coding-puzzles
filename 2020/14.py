import itertools
from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

def parse_mask(value):
    maskX = 0
    mask0 = 0
    mask1 = 0
    for i, value in enumerate(value[::-1]):
        bit = (1 << i)
        if value == 'X':
            maskX += bit
        elif value == '1':
            mask1 += bit
        elif value == '0':
            mask0 += bit
    return (maskX, mask0, mask1)

def parse_mem(op, value):
    addr = int(
        op.replace('mem[', '').replace(']', '')
    )
    value = int(value)
    return (addr, value)

def run(lines):
    memory = {}
    for line in lines:
        (op, value) = line.split(' = ')
        if op == 'mask':
            (maskX, _, mask1) = parse_mask(value)
        else:
            (addr, value) = parse_mem(op, value)
            memory[addr] = (value & maskX) | mask1

    return sum(memory.values())

example1 = multiline_lines(r"""
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
""")

run(example1) | eq(165)

run(input_lines) | debug('Star 1') | eq(8570568288597)

def run2(lines):
    memory = {}
    for line in lines:
        (op, value) = line.split(' = ')
        if op == 'mask':
            (maskX, mask0, mask1) = parse_mask(value)
        else:
            (addr, value) = parse_mem(op, value)

            stable_bits = ((addr & mask0) | mask1) & ~maskX
            floating_bits = [
                bit_value
                for (_, bit_value) in get_bits(maskX)
            ]
            for i in range(len(floating_bits) + 1):
                for combination in itertools.combinations(floating_bits, i):
                    floating_addr = stable_bits | sum(combination)
                    memory[floating_addr] = value

    return sum(memory.values())


example1 = multiline_lines(r"""
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
""")

run2(example1) | eq(208)

run2(input_lines) | debug('Star 2') | eq(3289441921203)
