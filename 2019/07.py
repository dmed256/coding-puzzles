import re
import itertools
from termcolor import colored
from advent_of_code import *

POSITION_MODE = 0
IMMEDIATE_MODE = 1

class IntProcessor:
    def __init__(self, values, input_values):
        if type(values) is str:
            self.original_values = split_comma_ints(values)
        else:
            self.original_values = values

        self.original_input_values = input_values.copy()

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

    def store_input(self):
        [pos] = self.extract_raw_values(1)
        self.values[pos] = self.input_values[0]
        self.input_values = self.input_values[1:]

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

    def unsafe_run(self):
        self.values = self.original_values.copy()
        self.input_values = self.original_input_values.copy()
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
                self.store_input()
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

    @staticmethod
    def run(values, input_values):
        p = IntProcessor(values, input_values)
        try:
            return p.unsafe_run()
        except Exception:
            p.debug_stack()

def run(values):
    values = split_comma_ints(values)

    cached_outputs = {}
    max_signal = 0
    for phase_settings in itertools.permutations([0, 1, 2, 3, 4]):
        last_output = 0
        for amp in range(5):
            inputs = [phase_settings[amp], last_output]
            key = (amp, *inputs)
            last_output = cached_outputs.get(
                key,
                IntProcessor.run(values, inputs)[-1],
            )
            cached_outputs[key] = last_output

        max_signal = max(max_signal, last_output)

    return max_signal

example1 = multiline_input(r"""
3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0
""")
example2 = multiline_input(r"""
3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0
""")
example3 = multiline_input(r"""
3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0
""")

run(example1) | eq(43210)
run(example2) | eq(54321)
run(example3) | eq(65210)

input_value = get_input()

run(input_value) | debug('Star 1')
