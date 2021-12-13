from repo_utils import *

input_lines = get_input_lines()

def run(lines):
    registers = defaultdict(int)

    registers['a'] = 7

    instructions = [
        [*line.split(), None]
        for line in lines
    ]

    def get_argc(instruction):
        return len([x for x in instruction[1:] if x is not None])

    ptr = 0
    while 0 <= ptr < len(instructions):
        ins, i1, i2, *_ = instructions[ptr]
        v1 = i1 and int_or(i1, registers[i1])
        v2 = i2 and int_or(i2, registers[i2])

        argc = get_argc(instructions[ptr])

        if ins == 'jnz' and argc == 2:
            ptr += v2 if v1 else 1
            continue
        elif ins == 'cpy' and argc == 2:
            registers[i2] = v1
        elif ins == 'inc' and argc == 1:
            registers[i1] += 1
        elif ins == 'dec' and argc == 1:
            registers[i1] -= 1
        elif ins == 'tgl' and argc == 1:
            ptr2 = ptr + v1
            if 0 <= ptr2 < len(instructions):
                ins2, *inputs = instructions[ptr2]
                argc = get_argc(instructions[ptr2])
                if argc == 1:
                    ins2 = 'dec' if ins2 == 'inc' else 'inc'
                    instructions[ptr2] = [ins2, *inputs]
                elif argc == 2:
                    ins2 = 'cpy' if ins2 == 'jnz' else 'jnz'
                    instructions[ptr2] = [ins2, *inputs]

        ptr += 1

    return registers['a']

def run2():
    pass

example1 = multiline_lines(r"""
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
""")

run(example1) | eq(3)

run(input_lines) | debug('Star 1') | eq(11340)

# run2() | submit(2)
