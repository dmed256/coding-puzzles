from repo_utils import *

input_lines = get_input_lines()

def apply_instruction(ins, a, b, c, input_registers):
    output_registers = list(input_registers)

    ra = input_registers[a]
    rb = input_registers[b]

    if ins == 'addr':
        output_registers[c] = ra + rb
    elif ins == 'addi':
        output_registers[c] = ra + b
    elif ins == 'mulr':
        output_registers[c] = ra * rb
    elif ins == 'muli':
        output_registers[c] = ra * b
    elif ins == 'banr':
        output_registers[c] = ra & rb
    elif ins == 'bani':
        output_registers[c] = ra & b
    elif ins == 'borr':
        output_registers[c] = ra | rb
    elif ins == 'bori':
        output_registers[c] = ra | b
    elif ins == 'setr':
        output_registers[c] = ra
    elif ins == 'seti':
        output_registers[c] = a
    elif ins == 'gtir':
        output_registers[c] = 1 if rb < a else 0
    elif ins == 'gtri':
        output_registers[c] = 1 if b < ra else 0
    elif ins == 'gtrr':
        output_registers[c] = 1 if rb < ra else 0
    elif ins == 'eqir':
        output_registers[c] = 1 if rb == a else 0
    elif ins == 'eqri':
        output_registers[c] = 1 if b == ra else 0
    elif ins == 'eqrr':
        output_registers[c] = 1 if rb == ra else 0
    else:
        raise 1

    return tuple(output_registers)

def run(problem, lines):
    reading_samples = True
    samples = []
    test_program = []

    ptr = 0
    while ptr < len(lines):
        line = lines[ptr]

        if not line.strip():
            ptr += 1
            continue

        if reading_samples and 'Before:' not in line:
            reading_samples = False

        if not reading_samples:
            test_program.append([
                int(x)
                for x in line.split()
            ])
            ptr += 1
            continue

        before = lines[ptr]
        instruction = lines[ptr + 1]
        after = lines[ptr + 2]
        ptr += 3

        before = before[:-1].replace('Before: [', '').split(', ')
        instruction = instruction.split()
        after = after[:-1].replace('After:  [', '').split(', ')

        instruction = [int(x) for x in instruction]
        before = tuple([int(x) for x in before])
        after = tuple([int(x) for x in after])

        samples.append((instruction, before, after))

    all_opcodes = {i for i in range(16)}
    possibilities = {
        'addr': deepcopy(all_opcodes),
        'addi': deepcopy(all_opcodes),
        'mulr': deepcopy(all_opcodes),
        'muli': deepcopy(all_opcodes),
        'banr': deepcopy(all_opcodes),
        'bani': deepcopy(all_opcodes),
        'borr': deepcopy(all_opcodes),
        'bori': deepcopy(all_opcodes),
        'setr': deepcopy(all_opcodes),
        'seti': deepcopy(all_opcodes),
        'gtir': deepcopy(all_opcodes),
        'gtri': deepcopy(all_opcodes),
        'gtrr': deepcopy(all_opcodes),
        'eqir': deepcopy(all_opcodes),
        'eqri': deepcopy(all_opcodes),
        'eqrr': deepcopy(all_opcodes),
    }
    opcode_map = {}

    ans1 = 0
    for instruction, before, expected_after in samples:
        opcode, a, b, c = instruction

        valid_ins = 0
        for ins, possible_opcodes in dict(possibilities).items():
            if opcode not in possible_opcodes:
                continue

            after = apply_instruction(ins, a, b, c, before)
            if after == expected_after:
                valid_ins += 1
                continue

            possibilities[ins].remove(opcode)

        if valid_ins >= 3:
            ans1 += 1

    if problem == 1:
        return ans1

    while possibilities:
        for ins, possible_opcodes in dict(possibilities).items():
            possibilities[ins] -= set(opcode_map.keys())

            if len(possible_opcodes) == 1:
                opcode_map[possible_opcodes.pop()] = ins
                del possibilities[ins]
                continue

    registers = (0, 0, 0, 0)
    for opcode, a, b, c in test_program:
        ins = opcode_map[opcode]
        registers = apply_instruction(ins, a, b, c, registers)

    return registers[0]

run(1, input_lines) | debug('Star 1') | eq(624)

run(2, input_lines) | debug('Star 2') | eq(584)
