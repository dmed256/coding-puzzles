import re
import textwrap
import itertools
from termcolor import colored
from advent_of_code import *
from int_processor import *

COMMANDS = {
    UP: 1,
    DOWN: 2,
    LEFT: 3,
    RIGHT: 4,
}

UNKNOWN = 0
FLOOR = 1
WALL = 2

W = 30
D = 2*W + 1

class System:
    def __init__(self):
        self.pos = (0, 0)
        self.oxygen_system = None
        self.grid = [UNKNOWN for i in range(D*D)]

        self.targets = set([
            apply_direction(self.pos, direction)
            for direction in DIRECTIONS
        ])
        self.target_path = []
        self.prev_target_paths = {}

        self.set_target()
        self.set_value(self.pos, FLOOR)

    @staticmethod
    def get_direction(pos, pos2):
        (x1, y1) = pos
        (x2, y2) = pos2

        if x1 < x2:
            return RIGHT
        if x1 > x2:
            return LEFT
        if y1 < y2:
            return UP
        if y1 > y2:
            return DOWN

    @staticmethod
    def get_index(pos):
        (x, y) = pos
        return (W + x) + (W + y)*D

    @staticmethod
    def get_pos(index):
        return (
            (index % D) - W,
            (index // D) - W,
        )

    def get_value(self, pos):
        return self.grid[self.get_index(pos)]

    def set_value(self, pos, value):
        self.grid[self.get_index(pos)] = value

    def update_targets(self):
        for direction in DIRECTIONS:
            pos2 = apply_direction(self.pos, direction)
            if self.get_value(pos2) != UNKNOWN:
                continue
            self.targets.add(pos2)

    def set_target(self):
        sorted_prev_targets = sorted(
            self.prev_target_paths.keys(),
            key=lambda target: len(self.prev_target_paths[target])
        )
        explore_prev_count = min(5, len(sorted_prev_targets))
        explore_prev_targets = sorted_prev_targets[:explore_prev_count]

        explore_new_targets = self.targets - set(self.prev_target_paths.keys())

        explore_targets = [
            *explore_prev_targets,
            *explore_new_targets
        ]
        if not explore_targets:
            explored_targets = self.targets

        target_paths = {
            target: path
            for target in explore_targets
            if len(path := self.get_path(self.pos, target)) > 1
        }
        if not target_paths:
            return

        self.target = min(
            target_paths.keys(),
            key=lambda target: len(target_paths[target])
        )

        # Remove current position from path
        self.target_path = target_paths[self.target][1:]

    def get_path(self, pos, target, end_paths=None, explored=None):
        end_paths = end_paths if end_paths is not None else {}
        explored = explored if explored is not None else set()

        if pos == target:
            return [pos]

        existing_path = end_paths.get(pos)
        if existing_path:
            return existing_path

        if pos in explored:
            return None

        explored.add(pos)

        found_paths = []
        for direction in DIRECTIONS:
            pos2 = apply_direction(pos, direction)

            if pos2 == target:
                return [pos, pos2]

            if self.get_value(pos2) != FLOOR:
                continue

            path = self.get_path(pos2, target, end_paths, explored)
            if path:
                found_paths.append(path)

        if found_paths:
            end_path = [pos] + min(found_paths, key=lambda x: len(x))
        else:
            end_path = None

        end_paths[pos] = end_path
        return end_path

    def get_input(self):
        if not self.target_path:
            self.set_target()

        if not self.target_path:
            self.p.is_done = True
            return COMMANDS[UP]

        direction = self.get_direction(self.pos, self.target_path[0])

        return COMMANDS[direction]

    def process_output(self, output):
        [code] = output

        # self.print_grid()
        # self.print_diagnostics()

        next_pos = self.target_path.pop(0)
        if next_pos in self.targets:
            self.targets.remove(next_pos)

        if code == 0:
            self.set_value(next_pos, WALL)
        elif code == 1:
            self.set_value(next_pos, FLOOR)
            self.pos = next_pos
            self.update_targets()
        elif code == 2:
            self.pos = next_pos
            self.update_targets()
            self.oxygen_system = next_pos

        return []

    def print_diagnostics(self):
        target_count = len(self.targets)
        explored_tiles = len([
            tile
            for tile in self.grid
            if tile != UNKNOWN
        ])
        positions = [
            self.get_pos(i)
            for i, tile in enumerate(self.grid)
            if tile != UNKNOWN
        ]
        x_min = min(x for (x, _) in positions)
        x_max = max(x for (x, _) in positions)
        y_min = min(y for (y, _) in positions)
        y_max = max(y for (y, _) in positions)

        if explored_tiles and not (explored_tiles % 100):
            print(f'target_count = {target_count}')
            print(f'explored_tiles = {explored_tiles}')
            print(f'GRID: ')
            print(f'  - X: [{x_min}, {x_max}]')
            print(f'  - Y: [{y_min}, {y_max}]')

    def print_grid(self):
        tile_to_ascii = {
            None: ' ',
            UNKNOWN: ' ',
            FLOOR: '.',
            WALL: '#',
        }

        def get_ascii(pos):
            if pos == self.pos:
                return green('D')
            if pos in self.targets:
                return yellow('*')

            tile = tile_to_ascii[self.get_value(pos)]
            if pos in self.target_path:
                return red(tile)
            else:
                return blue(tile)

        print('\n'.join([
            f'{y:03d} | ' + ' '.join([
                get_ascii((x, y))
                for x in range(-W, W + 1)
            ]) + ' |'
            for y in range(-W, W + 1)
        ]))

    def explore_map(self):
        print('EXPLORING MAP')
        input_value = get_input()
        self.p = IntProcessor(input_value, SINGLE_LOOP_MODE)

        self.p.get_input = self.get_input
        self.p.process_output = self.process_output
        self.p.run()

    def get_oxygen_system_path(self):
        min_path = self.get_path((0, 0), self.oxygen_system)
        return len(min_path) - 1

    def fill_oxygen(self):
        print('FILLING OXYGEN')
        missing = set([
            self.get_pos(i)
            for i, tile in enumerate(self.grid)
            if tile == FLOOR
        ])
        nodes = set([self.oxygen_system])

        minutes = 0
        while missing:
            new_nodes = set()
            for node in nodes:
                for direction in DIRECTIONS:
                    node2 = apply_direction(node, direction)
                    if node2 in missing:
                        new_nodes.add(node2)
                        missing.remove(node2)

            nodes = new_nodes
            minutes += 1

        return minutes



s = System()

tic()
s.explore_map()
toc('Explore map')

tic()
s.get_oxygen_system_path() | debug('Star 1')
toc('Star 1')

tic()
s.fill_oxygen() | debug('Star 1')
toc('Star 2')
