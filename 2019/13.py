import re
import textwrap
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

class Arcade:
    def __init__(self, interactive=False):
        input_value = get_input()
        self.p = IntProcessor(input_value, SINGLE_LOOP_MODE)

        self.interactive = interactive

        self.score = 0
        self.p.get_input = self.get_input
        self.p.process_output = self.process_output

        self.grid = {}
        self.grid_dims = None
        self.ball_x = None
        self.paddle_x = None

    def get_tiles(self):
        tile_count = len(self.p.output) // 3

        tiles = []
        for i in range(tile_count):
            x = self.p.output[3*i + 0]
            y = self.p.output[3*i + 1]
            value = self.p.output[3*i + 2]

            if x == -1 and y == 0:
                self.score = value
            else:
                tiles.append([x, y, value])

        return tiles

    def update_grid(self):
        tiles = self.get_tiles()

        for [x, y, tile] in tiles:
            self.grid[(x, y)] = tile

        if self.grid_dims is None:
            x_pos = [x for (x, _) in self.grid.keys()]
            y_pos = [y for (_, y) in self.grid.keys()]

            self.grid_dims = [
                [min(x_pos), max(x_pos)],
                [min(y_pos), max(y_pos)],
            ]

    def print_grid(self):
        [
            [x_min, x_max],
            [y_min, y_max],
        ] = self.grid_dims

        tile_to_ascii = {
            None: ' ',
            0: ' ',
            1: '|', # Walls are indestructible barriers.
            2: '=', # Blocks can be broken by the ball.
            3: '-', # The paddle is indestructible.
            4: 'o', # The ball moves diagonally and bounces off objects.
        }

        print(textwrap.dedent(f'''
        SCORE: {self.score}
        '''))

        print('\n'.join([
            f'{y:02d} ' + ' '.join([
                tile_to_ascii[self.grid.get((x, y))]
                for x in range(x_min, x_max + 1)
            ])
            for y in range(y_min, y_max + 1)
        ]))

    def get_input(self):
        # self.update_grid()
        # self.print_grid()

        if self.interactive:
            key = input()
            return {
                '': 0,
                's': -1,
                'f': 1,
            }[key]

        tiles = self.get_tiles()

        for [x, y, tile_type] in tiles:
            if tile_type == 4:
                self.ball_x = x
            elif tile_type == 3:
                self.paddle_x = x

        self.p.output = []

        if self.ball_x < self.paddle_x:
            return -1
        if self.paddle_x < self.ball_x:
            return 1
        return 0

    def process_output(self, output):
        # Update score
        self.get_tiles()
        return output

    def run(self, quarters=0):
        if quarters:
            self.p.original_values[0] = quarters
        self.p.run()

def run(interactive=False):
    arcade = Arcade(
        interactive=interactive
    )
    arcade.run()

    blocks = set()
    for [x, y, tile_type] in arcade.get_tiles():
        if tile_type == 2:
            blocks.add((x, y))

    return len(blocks)

run() | debug('Star 1')

def run2():
    arcade = Arcade()
    arcade.run(2)

    return arcade.score

run2() | debug('Star 2')