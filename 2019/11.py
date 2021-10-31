import re
import itertools
from termcolor import colored
from advent_of_code import *

POSITION_MODE = 0
IMMEDIATE_MODE = 1
RELATIVE_MODE = 2

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
        self.relative_base = 0
        self.stack = []

    def get_modes(self, count):
        modes = []
        for i in range(count):
            modes.append(self.mode % 10)
            self.mode = self.mode // 10
        return modes

    def pad_values(self, index):
        count = len(self.values)
        if index < count:
            return
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

    def get_pos_value(self, value, mode):
        if mode == POSITION_MODE:
            return value
        elif mode == IMMEDIATE_MODE:
            print('Unable to write to IMMEDIATE_MODE')
            raise 1
        elif mode == RELATIVE_MODE:
            return self.relative_base + value

    def set_value(self, index, value):
        self.pad_values(index)
        self.values[index] = value

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

    def extract_pos_values(self, count):
        raw_values = self.extract_raw_values(count)
        modes = self.get_modes(count)

        return [
            self.get_pos_value(raw_value, mode)
            for raw_value, mode in zip(raw_values, modes)
        ]

    def op_values(self, op):
        [v1, v2] = self.extract_values(2)
        [pos] = self.extract_pos_values(1)

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
        [pos] = self.extract_pos_values(1)

        input_value = self.get_input()
        self.set_value(pos, input_value)

        self.original_input_values[len(self.stack)] = input_value

    def store_output(self):
        [output] = self.extract_values(1)
        self.output.append(output)
        self.output = self.process_output(self.output)

    def update_relative_base(self):
        [output] = self.extract_values(1)
        self.relative_base += output

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

    def unsafe_run(self):
        # Reset
        if self.loop_mode == SINGLE_LOOP_MODE:
            self.is_done = False
            self.values = self.original_values.copy()
            self.ptr = 0
            self.stack = []
            self.relative_base = 0

        self.output = []

        operations = []
        while self.ptr < len(self.values):
            [instruction] = self.extract_raw_values(1)
            self.mode = instruction // 100
            op = instruction % 100

            operations.append(op)
            self.stack.append([self.ptr - 1, self.values.copy()])

            if op == 1:
                self.op_values('+')
            elif op == 2:
                self.op_values('*')
            elif op == 3:
                if self.loop_mode == FEEDBACK_LOOP_MODE: # and not self.input_values:
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

    def run(self):
        try:
            return self.unsafe_run()
        except Exception as e:
            print(f'Exception -> {e}')
            self.print_debug()
            raise e

input_value = get_input()

# Problem 1
# W = 500
# Problem 2
W = 45
D = 2*W + 1

UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)

DIRECTIONS = {
    # Counter-clockwise
    0: {
        UP: LEFT,
        LEFT: DOWN,
        DOWN: RIGHT,
        RIGHT: UP,
    },
    # Clockwise
    1: {
        UP: RIGHT,
        RIGHT: DOWN,
        DOWN: LEFT,
        LEFT: UP,
    }
}

DIRECTION_STR = {
    UP: 'UP',
    RIGHT: 'RIGHT',
    DOWN: 'DOWN',
    LEFT: 'LEFT',
}

class Problem:
    def __init__(self):
        # [-W, W] x [-W, W] grid
        self.grid = [0 for i in range(D * D)]
        self.robot_pos = [0, 0]
        self.robot_direction = UP

        # Problem 1:
        # self.set_value(self.robot_pos, 0)

        # Problem 2:
        self.set_value(self.robot_pos, 2)

    @staticmethod
    def get_pos(pos):
        [x, y] = pos
        return (W + x) + (W + y)*D

    def get_value(self, pos):
        return self.grid[self.get_pos(pos)]

    def set_value(self, pos, value):
        self.grid[self.get_pos(pos)] = value

    def process_output(self, output):
        if len(output) < 2:
            return output

        [paint, direction] = output

        current_paint = self.get_value(self.robot_pos)
        self.set_value(self.robot_pos, paint + 1)

        self.robot_direction = DIRECTIONS[direction][self.robot_direction]
        (dx, dy) = self.robot_direction
        self.robot_pos = [
            self.robot_pos[0] + dx,
            self.robot_pos[1] + dy,
        ]

        return []

    def print_grid(self):
        value_pixel = {
            0: ' ',
            1: blue('.'),
            2: yellow('#'),
        }

        pixels = [
            [
                value_pixel[self.get_value([x, y])]
                for x in range(-W, W + 1)
            ]
            for y in range(-W, W + 1)
        ]

        [x, y] = self.robot_pos
        pixels[W + y][W + x] = green({
            UP: '^',
            RIGHT: '>',
            DOWN: 'v',
            LEFT: '<',
        }[self.robot_direction])

        print('\n'.join([
            f'{i:02d} |' + ' '.join(row) + '|'
            for i, row in enumerate(reversed(pixels))
        ]))

    def get_input(self):
        # self.p.print_debug()
        # self.print_grid()
        # input()
        return {
            0: 0,
            1: 0,
            2: 1,
        }[self.get_value(self.robot_pos)]

    def run(self):
        self.p = IntProcessor(input_value, SINGLE_LOOP_MODE)
        self.p.get_input = lambda: self.get_input()
        self.p.process_output = lambda output: self.process_output(output)
        self.p.run()

        # Problem 2 only!
        self.print_grid()


p = Problem()
p.run()

# Wrong: 59
# Wrong: 86