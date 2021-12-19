from repo_utils import *
from utils import *

input_lines = get_input_lines()

def run(problem, lines):
    ip = 0
    ip_register = int(lines[0].split()[-1])
    registers = [0 for _ in range(6)]

    instructions = []
    for line in lines[1:]:
        ins, a, b, c = line.split()
        instructions.append((ins, int(a), int(b), int(c)))

    while True:
        ins, a, b, c = instructions[ip]

        registers = apply_instruction(ins, a, b, c, registers)
        registers[ip_register] += 1

        ip = registers[ip_register]
        if not (0 <= ip < len(instructions)):
            break

    return registers[0]

def run2(problem):
    # --------------------------------------------------#
    # Step 0: Assembly                                  #
    # --------------------------------------------------#
    # #ip 3
    # addi 3 16 3
    # seti 1 9 5
    # seti 1 1 4
    # mulr 5 4 2
    # eqrr 2 1 2
    # addr 2 3 3
    # addi 3 1 3
    # addr 5 0 0
    # addi 4 1 4
    # gtrr 4 1 2
    # addr 3 2 3
    # seti 2 3 3
    # addi 5 1 5
    # gtrr 5 1 2
    # addr 2 3 3
    # seti 1 4 3
    # mulr 3 3 3
    # addi 1 2 1
    # mulr 1 1 1
    # mulr 3 1 1
    # muli 1 11 1
    # addi 2 2 2
    # mulr 2 3 2
    # addi 2 20 2
    # addr 1 2 1
    # addr 3 0 3
    # seti 0 4 3
    # setr 3 9 2
    # mulr 2 3 2
    # addr 3 2 2
    # mulr 3 2 2
    # muli 2 14 2
    # mulr 2 3 2
    # addr 1 2 1
    # seti 0 6 0
    # seti 0 0 3

    # --------------------------------------------------#
    # Step 1: JS-formatted                              #
    # --------------------------------------------------#
    #  0 | IP = IP + 16
    #  1 | E  = 1
    #  2 | D  = 1
    #  3 | C  = E * D
    #  4 | C  = C == B
    #  5 | IP = C + IP
    #  6 | IP = IP + 1
    #  7 | A  = E + A
    #  8 | D  = D + 1
    #  9 | C  = D > B
    # 10 | IP = IP + C
    # 11 | IP = 2
    # 12 | E  = E + 1
    # 13 | C  = E > B
    # 14 | IP = C + IP
    # 15 | IP = 1
    # 16 | IP = IP * IP
    # 17 | B  = B + 2
    # 18 | B  = B * B
    # 19 | B  = IP * B
    # 20 | B  = B * 11
    # 21 | C  = C + 2
    # 22 | C  = C * IP
    # 23 | C  = C + 20
    # 24 | B  = B + C
    # 25 | IP = IP + A
    # 26 | IP = 0
    # 27 | C  = IP
    # 28 | C  = C * IP
    # 29 | C  = IP + C
    # 30 | C  = IP * C
    # 31 | C  = C * 14
    # 32 | C  = C * IP
    # 33 | B  = B + C
    # 34 | A  = 0
    # 35 | IP = 0

    # --------------------------------------------------#
    # Step 2: Replace IP                                #
    # --------------------------------------------------#
    # IP += 16    // 0  | ---[ 1 ]-->
    # E = 1       // 1  | <--[ 4 ]
    # D = 1       // 2  | <--[ 3 ]
    # C = E * D   // 3  | <--[ 2 ]
    # C = C == B  // 4  |
    # IP += C     // 5  | ??
    # IP += 1     // 6  | ??
    # A += E      // 7  |
    # D += 1      // 8  |
    # C = D > B   // 9  |
    # IP += C     // 10 | ??
    # IP = 2      // 11 | ---[ 2 ]-->
    # E += 1      // 12 |
    # C = E > B   // 13 |
    # IP += C     // 14 | <--[ 1 ]
    # IP = 1      // 15 | ---[ 3 ]-->
    # IP *= IP    // 16 | ??
    # B += 2      // 17 |
    # B *= B      // 18 |
    # B *= IP     // 19 |
    # B *= 11     // 20 |
    # C += 2      // 21 |
    # C *= IP     // 22 |
    # C += 20     // 23 |
    # B += C      // 24 |
    # IP += A     // 25 | ??
    # IP = 0      // 26 | ---[ 4 ]-->
    # C = IP      // 27 |
    # C *= IP     // 28 |
    # C += IP     // 29 |
    # C *= IP     // 30 |
    # C *= 14     // 31 |
    # C *= IP     // 32 |
    # B += C      // 33 |
    # A = 0       // 34 |
    # IP = 0      // 35 | ---[ 4 ]-->

    # --------------------------------------------------#
    # Step 3: JS-formatted                              #
    # --------------------------------------------------#
    # GOTO MAIN()
    #
    # START:
    #
    # E = 1
    # do {   // A
    #   D = 1
    #   do { // B
    #     if ((E * D) == B) {
    #       A += E
    #     } else {
    #       D += 1
    #     }
    #   } while (D <= B)
    #   E += 1
    # } while (E <= B)
    # C = 1
    #
    # RETURN
    #
    # MAIN:
    #
    # if (problem == 1) {
    #   B = 900
    # } else {
    #   B = 10221600
    # }
    # GOTO START

    # --------------------------------------------------#
    # Step 4: Python-formatted                          #
    # --------------------------------------------------#
    # if problem == 1:
    #     B = 900
    # else:
    #     B = 10551300
    #
    # A = 0
    # for E in range(1, B + 1):
    #     for D in range(1, B + 1):
    #         if (E * D) == B:
    #             A += E
    #
    # return A

    if problem == 1:
        B = 900
    else:
        B = 10551300

    return sum(sympy.divisors(B))

example1 = multiline_lines(r"""
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5
""")

run(1, example1) | eq(7)

run2(1) | debug('Star 1') | eq(2821)

run2(2) | debug('Star 2') | eq(30529296)
