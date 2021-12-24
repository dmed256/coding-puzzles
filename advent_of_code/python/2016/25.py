from repo_utils import *

input_lines = get_input_lines()

def parse_lines(lines):
    return [
        [*line.split(), None]
        for line in lines
    ]


def has_valid_signal(instructions, a):
    registers = defaultdict(int)
    registers['a'] = a

    ptr = 0
    outputs = []
    while 0 <= ptr < len(instructions):
        ins, i1, i2, *_ = instructions[ptr]
        v1 = i1 and int_or(i1, registers[i1])
        v2 = i2 and int_or(i2, registers[i2])

        if ins == 'jnz':
            ptr += v2 if v1 else 1
            continue
        elif ins == 'cpy':
            registers[i2] = v1
        elif ins == 'inc':
            registers[i1] += 1
        elif ins == 'dec':
            registers[i1] -= 1
        elif ins == 'out':
            if v1 != len(outputs) % 2:
                return False

            outputs.append(v1)
            if len(outputs) > 10:
                return True

        ptr += 1

def run(problem, lines):
    instructions = parse_lines(lines)

    a = 1
    while True:
        if has_valid_signal(instructions, a):
            return a
        a += 1

run(1, input_lines) | debug('Star 1') | eq(192)
