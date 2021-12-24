from repo_utils import *

input_lines = get_input_lines()

def run1(lines):
    registers = defaultdict(int)

    instructions = [
        [*line.split(), None]
        for line in lines
    ]

    ptr = 0
    while 0 <= ptr < len(instructions):
        ins, i1, i2, *_ = instructions[ptr]
        v1 = i1 and int_or(i1, registers[i1])
        v2 = i2 and int_or(i2, registers[i2])

        if ins == 'jnz':
            ptr += v2 if v1 else 1
            continue

        if ins == 'cpy':
            registers[i2] = v1
        elif ins == 'inc':
            registers[i1] += 1
        elif ins == 'dec':
            registers[i1] -= 1

        ptr += 1

    return registers['a']

def run2(problem):
    # cpy 1 a
    # cpy 1 b
    a = 1
    b = 1

    # cpy 26 d
    # jnz c 2
    # jnz 1 5
    # cpy 7 c
    # inc d
    # dec c
    # jnz c -2
    c = 0
    if problem == 1:
        d = 26
    else:
        d = 33

    # cpy a c
    # inc a
    # dec b
    # jnz b -2
    # cpy c b
    # dec d
    # jnz d -6
    for i in range(d):
        c = a
        a += b
        b = c

    # cpy 16 c
    # cpy 12 d
    # inc a
    # dec d
    # jnz d -2
    # dec c
    # jnz c -5
    return a + 16 * 12

example1 = multiline_lines(r"""
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a
""")

run1(example1) | eq(42)

run2(1) | debug('Star 1') | eq(318003)
run2(2) | debug('Star 2') | eq(9227657)
