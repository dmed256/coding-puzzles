from termcolor import colored
from advent_of_code import *

POSITION_MODE = 0
IMMEDIATE_MODE = 1
RELATIVE_MODE = 2

PAUSE = 'PAUSE'

class IntProcessor:
    def __init__(self, values, *, debug=False):
        if type(values) is str:
            self.original_values = split_comma_ints(values)
        else:
            self.original_values = values

        self.process_output = lambda x: x
        self.debug = debug

    def get_modes(self, count):
        modes = []
        for i in range(count):
            modes.append(self.mode % 10)
            self.mode = self.mode // 10
        return modes

    def pad_values(self, index):
        if index < len(self.values):
            return

        count = len(self.values)
        padding = [0 for i in range(index - count + 1)]
        self.values = [
            *self.values,
            *padding
        ]

    def get_value(self, value, mode):
        if mode == POSITION_MODE:
            self.pad_values(value)
            return self.values[value]
        elif mode == IMMEDIATE_MODE:
            return value
        elif mode == RELATIVE_MODE:
            pos = self.relative_base + value
            self.pad_values(pos)
            return self.values[pos]

    def set_value(self, index, value):
        self.pad_values(index)
        self.values[index] = value

    @profile
    def extract_raw_values(self, count):
        raw_values = self.values[self.ptr:(self.ptr + count)]
        self.ptr += count
        return raw_values

    def extract_values(self, count):
        raw_values = self.extract_raw_values(count)
        modes = self.get_modes(count)

        return [
            self.get_value(raw_value, mode)
            for raw_value, mode in zip(raw_values, modes)
        ]

    def extract_pos_value(self):
        [value] = self.extract_raw_values(1)
        [mode] = self.get_modes(1)

        if mode == POSITION_MODE:
            return value
        elif mode == RELATIVE_MODE:
            return self.relative_base + value
        elif mode == IMMEDIATE_MODE:
            print('Unable to write to IMMEDIATE_MODE')
            raise 1

    @profile
    def op_values(self, op):
        [v1, v2] = self.extract_values(2)
        pos = self.extract_pos_value()

        if op == '+':
            value = v1 + v2
        elif op == '*':
            value = v1 * v2
        elif op == '<':
            value = 1 if v1 < v2 else 0
        elif op == '==':
            value = 1 if v1 == v2 else 0

        self.set_value(pos, value)

    def jump_if_zero(self, cond):
        [value, pos] = self.extract_values(2)

        is_zero = value == 0
        if is_zero == cond:
            self.ptr = pos

    def store_input(self):
        pos = self.extract_pos_value()

        input_value = self.get_input()
        if input_value == PAUSE:
            self.is_paused = True
            self.pause_pos = pos
            return

        self.set_value(pos, input_value)

        if self.debug:
            self.original_input_values[len(self.stack)] = input_value

    def store_output(self):
        [output] = self.extract_values(1)
        self.output.append(output)
        self.output = self.process_output(self.output)

    def update_relative_base(self):
        [output] = self.extract_values(1)
        self.relative_base += output

    def print_debug(self):
        if not self.debug:
            print(red('Debug mode not set!'))
            raise 1

        stack = [
            *self.stack,
            [self.ptr, self.values.copy()]
        ]

        frame_count = len(stack) - 1

        # Get the place we errored out
        [_, values1] = stack[frame_count - 2]
        [ptr2, _] = stack[frame_count - 1]
        output_index = values1[ptr2 - 1]

        for frame in range(frame_count):
            if frame in self.original_input_values:
                print(yellow(f'inputs -> {self.original_input_values[frame]}'))

            [ptr, values1] = stack[frame]
            [ptr2, values2] = stack[frame + 1]

            output = []
            for i, (v1, v2) in enumerate(zip(values1, values2)):
                color = 'blue'
                if v1 != v2:
                    item = f'{v1} [{v2}]'
                    color = 'red'
                else:
                    item = str(v1)

                if i == output_index and (frame + 1) in self.original_input_values:
                    item = f'>>>{item}<<<'

                if ptr <= ptr2:
                    if ptr <= i < ptr2:
                        color = 'green'
                elif i in [ptr, ptr2]:
                    color = 'yellow'

                output.append(colored(item, color))

            print(f"[{', '.join(output)}]")

    def has_valid_output(self, op):
        if not self.output or self.output[-1] == 0:
            return True
        if op == 99:
            return True

        self.print_debug()

        return False

    def unsafe_run(self):
        self.is_done = False

        self.is_paused = False
        self.pause_pos = None

        self.original_input_values = {}
        self.values = self.original_values.copy()
        self.ptr = 0
        self.stack = []
        self.relative_base = 0
        self.output = []

        return self.loop_run()

    @profile
    def loop_run(self):
        while self.ptr < len(self.values):
            if self.is_done:
                break

            [instruction] = self.extract_raw_values(1)
            self.mode = instruction // 100
            op = instruction % 100

            if self.debug:
                self.stack.append([self.ptr - 1, self.values.copy()])

            if op == 1:
                self.op_values('+')
            elif op == 2:
                self.op_values('*')
            elif op == 3:
                self.store_input()
                if self.is_paused:
                    return None
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
            elif op == 9:
                self.update_relative_base()
            elif op == 99:
                self.is_done = True
                return self.output
            else:
                print(f'Operation [{op}] unknown!')
                self.print_debug()
                raise 1
                return None

    def unpause(self, input_value):
        self.set_value(self.pause_pos, input_value)

        if self.debug:
            self.original_input_values[len(self.stack)] = input_value

        self.is_paused = False
        self.pause_pos = None

        try:
            return self.loop_run()
        except Exception as e:
            print(f'Exception -> {e}')
            # self.print_debug()
            raise e

    def run(self, *, inputs=None):
        # Helper utils to iterate through hard-coded inputs
        if inputs is not None:
            inputs = inputs.copy()

            def get_input():
                return inputs.pop(0)

            def has_input_values():
                return len(inputs) > 0

            self.get_input = get_input
            self.has_input_values = has_input_values

        try:
            return self.unsafe_run()
        except Exception as e:
            print(f'Exception -> {e}')
            # self.print_debug()
            raise e