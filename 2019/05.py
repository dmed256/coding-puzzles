import re
from termcolor import colored
from advent_of_code import *

POSITION_MODE = 0
IMMEDIATE_MODE = 1

def split_code(values):
    return [
        int(x.strip())
        for x in values.split(',')
        if x
    ]

class IntProcessor:
    def __init__(self, values):
        if type(values) is str:
            self.original_values = split_code(values)
        else:
            self.original_values = values

        self.values = self.original_values

    def get_modes(self, count):
        modes = []
        mode = self.mode
        for i in range(count):
            modes.append(mode % 10)
            mode = mode // 10
        return modes

    def get_value(self, value, mode):
        if mode == POSITION_MODE:
            return self.values[value]
        elif mode == IMMEDIATE_MODE:
            return value

    def extract_raw_values(self, count):
        raw_values = [
            self.values[i]
            for i in range(self.ptr, self.ptr + count)
        ]
        self.ptr += count
        return raw_values

    def extract_values(self, count):
        raw_values = self.extract_raw_values(count)
        modes = self.get_modes(count)
        return [
            self.get_value(raw_value, mode)
            for raw_value, mode in zip(raw_values, modes)
        ]

    def op_values(self, op):
        [v1, v2] = self.extract_values(2)
        [pos] = self.extract_raw_values(1)

        if op == '+':
            value = v1 + v2
        elif op == '*':
            value = v1 * v2
        elif op == '<':
            value = 1 if v1 < v2 else 0
        elif op == '==':
            value = 1 if v1 == v2 else 0

        self.values[pos] = value

    def jump_if_zero(self, cond):
        [value, pos] = self.extract_values(2)

        is_zero = value == 0
        if is_zero == cond:
            self.ptr = pos

    def store_input(self, input_value):
        [pos] = self.extract_raw_values(1)
        self.values[pos] = input_value

    def store_output(self):
        [output] = self.extract_values(1)
        self.output.append(output)

    def debug_stack(self):
        self.stack.append([self.ptr, self.values.copy()])

        frame_count = len(self.stack) - 1

        # Get the place we errored out
        [_, values1] = self.stack[frame_count - 2]
        [ptr2, _] = self.stack[frame_count - 1]
        output_index = values1[ptr2 - 1]

        for i in range(frame_count):
            [ptr, values1] = self.stack[i]
            [ptr2, values2] = self.stack[i + 1]

            output = []
            for i, (v1, v2) in enumerate(zip(values1, values2)):
                color = 'blue'
                if v1 != v2:
                    item = f'{v1} [{v2}]'
                    color = 'red'
                else:
                    item = str(v1)

                if ptr <= i < ptr2:
                    color = 'green'
                elif i == output_index:
                    item = f'>>>{item}<<<'
                    color = 'yellow'

                output.append(colored(item, color))

            print(f"[{', '.join(output)}]")

    def has_valid_output(self, op):
        if not self.output or self.output[-1] == 0:
            return True
        if op == 99:
            return True

        # self.debug_stack()

        return False

    def unsafe_run(self, input_value):
        self.values = self.original_values.copy()
        self.ptr = 0
        self.output = []
        self.stack = []

        operations = []
        while self.ptr < len(self.values):
            [instruction] = self.extract_raw_values(1)
            self.mode = instruction // 100
            op = instruction % 100

            operations.append(op)
            self.stack.append([self.ptr - 1, self.values.copy()])
            if not self.has_valid_output(op):
                return self.output

            if op == 1:
                self.op_values('+')
            elif op == 2:
                self.op_values('*')
            elif op == 3:
                self.store_input(input_value)
            elif op == 4:
                self.store_output()
            elif op == 5:
                self.jump_if_zero(False)
            elif op == 6:
                self.jump_if_zero(True)
            elif op == 7:
                self.op_values('<')
            elif op == 8:
                self.op_values('==')
            elif op == 99:
                if operations[-2] == 4:
                    return self.output
                else:
                    return None
            else:
                print(f'Operation [{op}] unknown!')
                self.debug_stack()
                return None

    def run(self, input_value):
        try:
            return self.unsafe_run(input_value)
        except Exception:
            self.debug_stack()

def extract_values(values, ptr, count, mode):
    p = IntProcessor(values)
    p.ptr = ptr
    p.mode = mode

    return p.extract_values(count)

def run(values, input_value):
    return IntProcessor(values).run(input_value)

extract_values(
    [2, 0, 1], 0, 2, 0
) | should_be([1, 2])

extract_values(
    [2, 0, 1], 0, 2, 1
) | should_be([2, 2])

extract_values(
    [2, 0, 1], 0, 2, 10
) | should_be([1, 0])

extract_values(
    [2, 0, 1], 0, 2, 11
) | should_be([2, 0])

example1 = split_code('3,0,4,0,99')
for i in range(100):
    run(example1, i) | should_be([i])

input_value = split_code(get_input())

run(input_value, 1) | debug('Star 1')

less_than_8 = """
3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99
"""

for i in range(8):
    run(less_than_8, i)[-1] | eq(999)

run(less_than_8, 8)[-1] | eq(1000)

for i in range(9, 100):
    run(less_than_8, i)[-1] | eq(1001)

run(input_value, 5) | debug('Star 2')
