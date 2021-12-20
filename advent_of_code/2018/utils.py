def apply_instruction(ins, a, b, c, input_registers):
    output_registers = list(input_registers)

    if 0 <= a < len(input_registers):
        ra = input_registers[a]
    else:
        ra = None

    if 0 <= b < len(input_registers):
        rb = input_registers[b]
    else:
        rb = None

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
        output_registers[c] = 1 if a > rb else 0
    elif ins == 'gtri':
        output_registers[c] = 1 if ra > b else 0
    elif ins == 'gtrr':
        output_registers[c] = 1 if ra > rb else 0
    elif ins == 'eqir':
        output_registers[c] = 1 if a == rb else 0
    elif ins == 'eqri':
        output_registers[c] = 1 if ra == b else 0
    elif ins == 'eqrr':
        output_registers[c] = 1 if ra == rb else 0
    else:
        raise 1

    return output_registers
