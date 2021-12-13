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
    # --------------------------------------------------#
    # Step 0: Assembly                                  #
    # --------------------------------------------------#
    # cpy a b
    # dec b
    # cpy a d
    # cpy 0 a
    # cpy b c  [0, d] <-
    # inc a    [1, c] <-
    # dec c
    # jnz c -2 [1, c] ->
    # dec d
    # jnz d -5 [0, d] ->
    # dec b
    # cpy b c
    # cpy c d
    # dec d    [2, d] <-
    # inc c
    # jnz d -2 [2, d] ->
    # tgl c    ????
    # cpy -16 c
    # jnz 1 c  [3, 1] -> c ???
    # cpy 84 c
    # jnz 75 d [4, 1] -> d ???  [6, c] <-
    # inc a    [5, d] <-
    # inc d
    # jnz d -2 [5, d] ->
    # inc c
    # jnz c -5 [6, c] ->

    # --------------------------------------------------#
    # Step 1: JS-formatted                              #
    # --------------------------------------------------#
    # a = 12
    # b = a
    # b -= 1
    #
    # do {
    #   d = a
    #   a = 0
    #
    #   do {
    #     c = b
    #     do {
    #       a += 1
    #       c -= 1
    #     } while (c)
    #     d -= 1
    #   } while (d)
    #
    #   b -= 1
    #   c = b
    #   d = b
    #
    #   do {
    #     d -= 1
    #     c += 1
    #   } while (d)
    #
    #   tgl c
    #   // +-----------------------------------------------------+
    #   // |                                                     |
    #   // |   Problem 1:                                        |
    #   // |     - Changes "jnz c -5" -> "cpy c -5" at the end   |
    #   // |                                                     |
    #   // |   Problem 2:                                        |
    #   // |     - No-op (out of bounds)                         |
    #   // |                                                     |
    #   // +-----------------------------------------------------+
    #
    #   c = -16
    # } while (c)
    #
    # c = 84
    #
    # do {
    #   goto [d] ???
    #
    #   do {
    #     a += 1
    #     d += 1
    #   } while(d)
    #
    #   c += 1
    # } while(c)

    # --------------------------------------------------#
    # Step 2: Manually computed expressions             #
    # --------------------------------------------------#
    # // Passes:
    # // a = mult(11, 12), mult(10, 12), mult(9, 12), ...
    # // b = 10,  9,  8, ...
    # // c = 20, 18, 16, ...
    # // d = 0
    #
    # // tgl c
    # // +-----------------------------------------------------+
    # // |                                                     |
    # // |   Problem 1:                                        |
    # // |     - Changes "jnz c -5" -> "cpy c -5" at the end   |
    # // |                                                     |
    # // |   Problem 2:                                        |
    # // |     - Changes every even instruction after tgl      |
    # // |                                                     |
    # // +-----------------------------------------------------+
    #
    # // Problem 1:
    # // |
    # // |  tgl c
    # // |  cpy -16 c
    # // |  jnz 1 c  [3, 1] -> c ???
    # // |  cpy 84 c
    # // |  jnz 75 d [4, 1] -> d ???  [6, c] <-
    # // |  inc a    [5, d] <-
    # // |  inc d
    # // |  jnz d -2 [5, d] ->
    # // |  inc c
    # // |  cpy c -5
    # // |
    #
    # // Problem 2:
    # // |
    # // | inc c
    # // | cpy -16 c
    # // | cpy 1 c
    # // | cpy 84 c
    # // | cpy 75 d [6, c] <-
    # // | inc a    [5, d] <-
    # // | dec d
    # // | jnz d -2 [5, d] ->
    # // | dec c
    # // | jnz c -5 [6, c] ->
    # // |
    #
    # // ->
    # //
    # // a = mult(11, 12), mult(10, 12), mult(9, 12), ...
    # // b = 10,  9,  8, ...
    # // c = 20, 18, 16, ...
    # // d = 0
    #
    # c = 84
    # do {
    #   d = 75
    #   do {
    #     a += 1
    #     d -= 1
    #   } while (d)
    #   c -= 1
    # } while (c)


    # --------------------------------------------------#
    # Step 3: Manually computed last bits               #
    # --------------------------------------------------#
    a = mult(range(1, 13))
    a += 75 * 84

    return a

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

run2() | submit(2)
