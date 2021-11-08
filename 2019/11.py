import re
import itertools
from termcolor import colored
from advent_of_code import *
from int_processor import *

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
    def __init__(self, *, star):
        # [-W, W] x [-W, W] grid
        self.grid = [0 for i in range(D * D)]
        self.robot_pos = [0, 0]
        self.robot_direction = UP

        self.star = star
        if star == 1:
            self.set_value(self.robot_pos, 0)
        else:
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
        self.p = IntProcessor(input_value)
        self.p.get_input = self.get_input
        self.p.process_output = self.process_output
        self.p.run()

        if self.star == 2:
            self.print_grid()

input_value = get_input()

W = 500
D = 2*W + 1

p = Problem(star=1)
p.run()
sum([
    1
    for value in p.grid
    if value
]) | debug('Star 1')

W = 45
D = 2*W + 1

p = Problem(star=2)
p.run()
