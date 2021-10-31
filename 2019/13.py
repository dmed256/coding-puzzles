import re
import textwrap
import itertools
from termcolor import colored
from advent_of_code import *
from int_processor import *

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
