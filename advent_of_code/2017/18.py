from repo_utils import *

input_value = get_input()
input_lines = get_input_lines()

class Problem:
    def __init__(self, problem, lines, program_id=0):
        self.problem = problem
        self.program_id = program_id

        self.instructions = []
        for line in lines:
            [ins, *inputs] = line.split(' ')
            if len(inputs) == 1:
                inputs += [None]

            [v1, v2] = inputs

            if v1:
                v1 = int_or(v1, v1)
            if v2:
                v2 = int_or(v2, v2)

            self.instructions.append((ins, v1, v2))

        self.registers = {
            letter: 0
            for letter in string.ascii_lowercase
        }
        self.registers['p'] = program_id

        self.ptr = 0

        self.done = False
        self.halted = False

        self.sent_values = []
        self.received_values = []

    def get_value(self, v):
        if v is None:
            return None

        if type(v) is int:
            return v

        return self.registers[v]

    def send(self, value):
        self.sent_values.append(value)
        if self.problem == 2:
            self.other_program.received_values.append(value)

    def can_receive(self):
        if self.problem == 1:
            return True
        else:
            return bool(self.received_values)

    def receive(self, register, value):
        if self.problem == 1:
            if value != 0 and self.sent_values:
                self.received_values.append(self.sent_values[-1])
        else:
            value = self.received_values.pop(0)
            self.registers[register] = value

    def step(self):
        if self.ptr >= len(self.instructions):
            self.halted = True
            self.done = True
            return

        ins, i1, i2 = self.instructions[self.ptr]

        v1 = self.get_value(i1)
        v2 = self.get_value(i2)

        if ins == 'jgz':
            if v1 > 0:
                self.ptr += v2
            else:
                self.ptr += 1
            return

        if ins == 'snd':
            self.send(v1)
        elif ins == 'set':
            self.registers[i1] = v2
        elif ins == 'add':
            self.registers[i1] += v2
        elif ins == 'mul':
            self.registers[i1] *= v2
        elif ins == 'mod':
            self.registers[i1] %= v2
        elif ins == 'rcv':
            if not self.can_receive():
                self.halted = True
                return
            self.receive(i1, v1)

        self.ptr += 1

    def can_resume(self):
        if self.done:
            return False

        if not self.halted:
            return True

        return self.can_receive()

    def resume(self):
        if not self.can_resume():
            return

        self.halted = False
        while not self.halted:
            self.step()

    def run1(self):
        while not self.received_values:
            self.step()
        return self.received_values[0]

def run(*args):
    return Problem(1, *args).run1()

def run2(*args):
    p0 = Problem(2, *args, 0)
    p1 = Problem(2, *args, 1)

    p0.other_program = p1
    p1.other_program = p0

    while p0.can_resume() or p1.can_resume():
        p0.resume()
        p1.resume()

    return len(p1.sent_values)

example1 = multiline_lines(r"""
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2
""")

example2 = multiline_lines(r"""
snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d
""")

run(example1) | eq(4)

run(input_lines) | debug('Star 1') | eq(2951)

run2(example2) | eq(3)

run2(input_lines) | debug('Star 2') | eq(7366)
