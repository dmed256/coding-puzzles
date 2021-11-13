import re
import itertools
from termcolor import colored
from advent_of_code import *
from int_processor import *

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

class Problem:
    def __init__(self, problem):
        W = 50
        D = 2*W + 1

        # [-W, W] x [-W, W] grid
        self.grid = Grid([
            [0 for x in range(D)]
            for y in range(D)
        ])
        self.robot_pos = (W, W)
        self.robot_direction = UP

        self.grid[self.robot_pos] = (
            0
            if problem == 1 else
            2
        )

    def process_output(self, output):
        if len(output) < 2:
            return output

        [paint, rotation] = output

        current_paint = self.grid[self.robot_pos]
        self.grid[self.robot_pos] = paint + 1

        self.robot_direction = (
            COUNTER_CLOCKWISE
            if rotation == 0 else
            CLOCKWISE
        )[self.robot_direction]

        self.robot_pos = self.grid.apply_direction(
            self.robot_pos,
            self.robot_direction,
        )

        return []

    def get_input(self):
        return {
            0: 0,
            1: 0,
            2: 1,
        }[self.grid[self.robot_pos]]

    def print_grid(self):
        grid = self.grid.copy()

        value_pixel = {
            0: ' ',
            1: blue('.'),
            2: yellow('#'),
        }
        for pos, v in self.grid:
            grid[pos] = value_pixel[v]

        grid[self.robot_pos] = {
            UP: '^',
            RIGHT: '>',
            DOWN: 'v',
            LEFT: '<',
        }[self.robot_direction]
        grid.print()

    def run(self):
        self.p = IntProcessor(input_value)
        self.p.get_input = self.get_input
        self.p.process_output = self.process_output
        self.p.run()

input_value = get_input()

p = Problem(1)
p.run()
sum([
    1
    for pos, v in p.grid
    if v
]) | debug('Star 1') | eq(2252)

p = Problem(2)
p.run()
p.print_grid()