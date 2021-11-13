from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

def get_instructions(lines):
    return [
        (values[0], int(values[1]))
        for line in lines
        if (values := line.split(' '))
    ]

def run_program(instructions):
    ptr = 0
    acc = 0
    instructions_ran = set()
    count = len(instructions)
    while True:
        if ptr in instructions_ran or ptr >= count:
            break

        (op, value) = instructions[ptr]
        instructions_ran.add(ptr)

        if op == 'acc':
            acc += value
            ptr += 1
        elif op == 'jmp':
            ptr += value
        else:
            ptr += 1

    finished = (
        (count - 2 in instructions_ran) and
        (count - 1 in instructions_ran) and
        ptr == count
    )

    return [acc, finished]

def run(lines):
    instructions = get_instructions(lines)
    [acc, finished] = run_program(instructions)
    return acc

example1 = multiline_lines(r"""
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
""")

run(example1) | eq(5)

run(input_lines) | debug('Star 1') | eq(1446)

def run2(lines):
    instructions = get_instructions(lines)
    potential_swaps = [
        i
        for i, [op, value] in enumerate(instructions)
        if op in ['nop', 'jmp']
    ]
    swap_op = {
        'nop': 'jmp',
        'jmp': 'nop',
    }

    for i in potential_swaps:
        fixed_instructions = instructions.copy()
        (op, value) = fixed_instructions[i]
        fixed_instructions[i] = (swap_op[op], value)

        [acc, finished] = run_program(fixed_instructions)
        if finished:
            break

    return acc

run2(example1) | eq(8)

run2(input_lines) | debug('Star 2') | eq(1403)
