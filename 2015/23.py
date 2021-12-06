from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

class Problem:
    def __init__(self, problem, lines, init_registers, register):
        self.problem = problem
        self.init_registers = init_registers
        self.register = register

        instructions = []
        for line in lines:
            [ins, *other] = line.split(' ')
            inputs = ' '.join(other).strip()

            register, value = None, None
            if ',' in inputs:
                register, value = inputs.split(', ')
            elif inputs in ['a', 'b']:
                register = inputs
            else:
                value = inputs

            if value:
                sign = 1 if value[0] == '+' else -1
                value = sign * int(value[1:])

            instructions.append([ins, register, value])

        self.instructions = instructions

    def run(self):
        registers = deepcopy(self.init_registers)

        ptr = 0
        while 0 <= ptr < len(self.instructions):
            [ins, register, value] = self.instructions[ptr]

            if ins == 'hlf':
                registers[register] //= 2
                ptr += 1
            elif ins == 'tpl':
                registers[register] *= 3
                ptr += 1
            elif ins == 'inc':
                registers[register] += 1
                ptr += 1
            elif ins == 'jmp':
                ptr += value
            elif ins == 'jie':
                if registers[register] % 2 == 0:
                    ptr += value
                else:
                    ptr += 1
            elif ins == 'jio':
                if registers[register] == 1:
                    ptr += value
                else:
                    ptr += 1

        return registers[self.register]

def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

example1 = multiline_lines(r"""
inc a
jio a, +2
tpl a
inc a
""")

registers1 = {
    'a': 0,
    'b': 0,
}

registers2 = {
    'a': 1,
    'b': 0,
}

run(example1, registers1, 'a') | eq(2)

run(input_lines, registers1, 'b') | debug('Star 1') | eq(307)

run2(input_lines, registers2, 'b') | debug('Star 2') | eq(160)
