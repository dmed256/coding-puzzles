import re
import itertools
from termcolor import colored
from advent_of_code import *

POSITION_MODE = 0
IMMEDIATE_MODE = 1

SINGLE_LOOP_MODE = 0
FEEDBACK_LOOP_MODE = 1

class IntProcessor:
    def __init__(self, values, loop_mode):
        if type(values) is str:
            self.original_values = split_comma_ints(values)
        else:
            self.original_values = values

        self.is_done = False
        self.loop_mode = loop_mode
        self.values = self.original_values.copy()
        self.original_input_values = {}
        self.input_values = []
        self.ptr = 0
        self.stack = []

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

    def print_debug(self):
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

    def unsafe_run(self, input_values):
        # Reset
        if self.loop_mode == SINGLE_LOOP_MODE:
            self.is_done = False
            self.values = self.original_values.copy()
            self.ptr = 0
            self.stack = []

        self.original_input_values[len(self.stack)] = input_values.copy()
        self.input_values = input_values.copy()
        self.output = []

        operations = []
        while self.ptr < len(self.values):
            [instruction] = self.extract_raw_values(1)
            self.mode = instruction // 100
            op = instruction % 100

            operations.append(op)
            self.stack.append([self.ptr - 1, self.values.copy()])

            if (self.loop_mode != FEEDBACK_LOOP_MODE and
                not self.has_valid_output(op)):
                return None

            if op == 1:
                self.op_values('+')
            elif op == 2:
                self.op_values('*')
            elif op == 3:
                if self.loop_mode == FEEDBACK_LOOP_MODE and not self.input_values:
                    self.stack.pop()
                    self.ptr -= 1
                    return self.output
                self.store_input()
            elif op == 4:
                self.store_output()
                if self.loop_mode == FEEDBACK_LOOP_MODE:
                    return self.output
            elif op == 5:
                self.jump_if_zero(False)
            elif op == 6:
                self.jump_if_zero(True)
            elif op == 7:
                self.op_values('<')
            elif op == 8:
                self.op_values('==')
            elif op == 99:
                self.is_done = True
                if len(operations) > 2 and operations[-2] == 4:
                    return self.output
                elif self.loop_mode == FEEDBACK_LOOP_MODE:
                    # Not an error in feedback loop
                    return None
                else:
                    print('Invalid [99], no output!')
                    self.print_debug()
                    raise 1
                    return None
            else:
                print(f'Operation [{op}] unknown!')
                self.print_debug()
                raise 1
                return None

    def run(self, input_values):
        try:
            return self.unsafe_run(input_values)
        except Exception as e:
            print(f'Exception -> {e}')
            self.print_debug()
            raise e

def get_signal(
        values,
        loop_mode,
        phase_settings,
):
    amplifier_processors = [
        IntProcessor(values, loop_mode)
        for i in range(5)
    ]
    p_inputs = [
        [phase_setting]
        for phase_setting in phase_settings
    ]

    is_done = False
    signal = 0
    last_output = 0
    while not is_done:
        for amp in range(5):
            processor = amplifier_processors[amp]
            if processor.is_done:
                continue

            inputs = [*p_inputs[amp], last_output]

            outputs = processor.run(inputs)
            if outputs:
                last_output = outputs[-1]
                # Get the output from the last amplifier
                if amp == 4:
                    signal = last_output

            p_inputs[amp] = []

            if processor.is_done:
                is_done = amp == 4
                continue

            if outputs is None:
                processor.print_debug()
                raise 1
                break

    return signal

def run(values, loop_mode, phase_setting_sequence):
    values = split_comma_ints(values)

    max_signal = 0
    for phase_settings in itertools.permutations(phase_setting_sequence):
        signal = get_signal(
            values,
            loop_mode,
            phase_settings,
        )
        if signal is not None:
            max_signal = max(max_signal, signal)

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

run(
    example1,
    SINGLE_LOOP_MODE,
    [0, 1, 2, 3, 4],
) | eq(43210)

run(
    example2,
    SINGLE_LOOP_MODE,
    [0, 1, 2, 3, 4],
) | eq(54321)

run(
    example3,
    SINGLE_LOOP_MODE,
    [0, 1, 2, 3, 4],
) | eq(65210)

input_value = get_input()

run(
    input_value,
    SINGLE_LOOP_MODE,
    [0, 1, 2, 3, 4],
) | debug('Star 1')

example1 = multiline_input("""
3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
""")
example2 = multiline_input("""
3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10
""")

run(
    example1,
    FEEDBACK_LOOP_MODE,
    [5, 6, 7, 8, 9],
) | eq(139629729)

run(
    example2,
    FEEDBACK_LOOP_MODE,
    [5, 6, 7, 8, 9],
) | eq(18216)

run(
    input_value,
    FEEDBACK_LOOP_MODE,
    [5, 6, 7, 8, 9],
) | debug('Star 2')