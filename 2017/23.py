from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

def run(lines):
    instructions = []
    for line in lines:
        if line[0] == '#':
            continue
        ins, a, b = line.split(' ')
        a = int_or(a, a)
        b = int_or(b, b)

        instructions.append((ins, a, b))

    registers = {
        l: 0
        for l in 'abcdefgh'
    }

    ptr = 0
    mults = 0
    while 0 <= ptr < len(instructions):
        ins, a, b = instructions[ptr]

        if ins == 'jnz':
            if registers.get(a, a) != 0:
                ptr += registers.get(b, b)
                continue

        if ins == 'set':
            registers[a] = registers.get(b, b)
        elif ins == 'sub':
            registers[a] -= registers.get(b, b)
        elif ins == 'mul':
            registers[a] -= registers.get(b, b)
            mults += 1

        ptr += 1

    return mults

def run2():
    # Pythonified code:
    #
    # b = 107900
    # c = b + 17000
    # while True:
    #     f = 1
    #     d = 2
    #     while True:
    #         e = 2
    #         while True:
    #             g = (d * e) - b
    #             if g == 0:
    #                 f = 0
    #             e += 1
    #             g = e - b
    #             if not g:
    #                 break
    #
    #         d += 1
    #         g = d - b
    #         if not g:
    #             break
    #
    #     if not f:
    #         h += 1
    #
    #     g = b - c
    #     if not g:
    #         return h
    #
    #     b += 17

    # Simplified version:
    start = 107900
    end = start + 17000

    primes = get_primes_before(end)

    return len([
        1
        for i in range(1001)
        if start + (17 * i) not in primes
    ])

run(input_lines) | debug('Star 1') | eq(5929)

run2() | debug('Star 2') | eq(907)
