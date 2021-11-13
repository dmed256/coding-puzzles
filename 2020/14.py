from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

def parse_mask(value):
    and_mask = 0
    or_mask = 0
    for i, value in enumerate(value[::-1]):
        bit = (1 << i)
        if value == 'X':
            and_mask += bit
        elif value == '1':
            or_mask += bit
    return and_mask, or_mask

def run(lines):
    memory = {}
    for line in lines:
        (op, value) = line.split(' = ')
        if op == 'mask':
            and_mask, or_mask = parse_mask(value)
        else:
            addr = int(
                op.replace('mem[', '').replace(']', '')
            )
            value = int(value)
            memory[addr] = (value & and_mask) | or_mask

    return sum(memory.values())

example1 = multiline_lines(r"""
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
""")

run(example1) | eq(165)

run(input_lines) | debug('Star 1') | eq(8570568288597)

# run2(example1) | eq()

# run2(input_lines) | debug('Star 2')
