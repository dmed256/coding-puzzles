from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

class Problem:
    def __init__(self, problem, lines):
        self.problem = problem

        instructions = []
        for line in lines:
            [word1, ins, shift, _if, word2, comp, bound] = line.split()
            shift = int(shift)
            bound = int(bound)

            if ins == 'dec':
                shift = -shift

            cond = (word2, comp, bound)
            op = (word1, shift)
            instructions.append((cond, op))

        self.instructions = instructions

    def run(self):
        registers = {}
        max_value = None
        for cond, op in self.instructions:
            reg1, comp, bound = cond
            if reg1 not in registers:
                registers[reg1] = 0
            reg1 = registers[reg1]

            if comp == '>=':
                passes = reg1 >= bound
            elif comp == '>':
                passes = reg1 > bound
            elif comp == '<=':
                passes = reg1 <= bound
            elif comp == '<':
                passes = reg1 < bound
            elif comp == '==':
                passes = reg1 == bound
            elif comp == '!=':
                passes = reg1 != bound

            if not passes:
                continue

            reg2, shift = op
            if reg2 not in registers:
                registers[reg2] = 0

            registers[reg2] += shift
            max_value = safe_max(max_value, registers[reg2])

        if self.problem == 1:
            return max(registers.values())
        else:
            return max_value

def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

example1 = multiline_lines(r"""
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
""")

run(example1) | eq(1)

run(input_lines) | debug('Star 1') | eq(4877)

run2(example1) | eq(10)

run2(input_lines) | debug('Star 2') | eq(5471)
