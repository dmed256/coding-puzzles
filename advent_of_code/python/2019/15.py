import re
import textwrap
import itertools
from functools import lru_cache
from termcolor import colored
from repo_utils import *
from int_processor import *

COMMANDS = {
    GRID_UP: 1,
    GRID_DOWN: 2,
    GRID_LEFT: 3,
    GRID_RIGHT: 4,
}

UNKNOWN = ' '
FLOOR = '.'
WALL = '#'

W = 30
D = 2*W + 1

class System:
    def __init__(self):
        self.pos = (W, W)
        self.oxygen_system = None
        self.grid = Grid([
            [UNKNOWN for x in range(D)]
            for y in range(D)
        ])

        self.targets = {
            apply_direction(self.pos, direction)
            for direction in GRID_DIRECTIONS
        }
        self.target_path = []
        self.prev_target_paths = {}

        self.set_target()
        self.grid[self.pos] = FLOOR

    @staticmethod
    def get_direction(pos, pos2):
        (x1, y1) = pos
        (x2, y2) = pos2

        if x1 < x2:
            return GRID_RIGHT
        if x1 > x2:
            return GRID_LEFT
        if y1 < y2:
            return GRID_UP
        if y1 > y2:
            return GRID_DOWN

    def update_targets(self):
        for direction in GRID_DIRECTIONS:
            pos2 = apply_direction(self.pos, direction)
            if self.grid[pos2] != UNKNOWN:
                continue
            self.targets.add(pos2)

    def set_target(self):
        explored_nodes = {self.pos}
        paths = [
            [self.pos]
        ]
        self.target_path = None
        while paths and not self.target_path:
            next_paths = []
            for path in paths:
                pos = path[-1]

                neighbors = [
                    n
                    for direction in GRID_DIRECTIONS
                    if (n := self.grid.apply_direction(pos, direction))
                    and self.grid[n] != WALL
                    and n not in explored_nodes
                ]
                if not neighbors:
                    continue

                unknowns = [
                    n
                    for n in neighbors
                    if self.grid[n] == UNKNOWN
                ]
                if unknowns:
                    # Remove current position from path
                    self.target_path = [*path[1:], unknowns[0]]
                    break

                for n in neighbors:
                    next_paths.append([*path, n])
                    explored_nodes.add(n)

            paths = next_paths

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
        for direction in GRID_DIRECTIONS:
            pos2 = apply_direction(pos, direction)

            if pos2 == target:
                return [pos, pos2]

            if self.grid[pos2] != FLOOR:
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
            return COMMANDS[GRID_UP]

        direction = self.get_direction(self.pos, self.target_path[0])

        return COMMANDS[direction]

    def process_output(self, output):
        [code] = output

        # self.grid.print()
        # self.print_diagnostics()

        next_pos = self.target_path.pop(0)
        if next_pos in self.targets:
            self.targets.remove(next_pos)

        if code == 0:
            self.grid[next_pos] = WALL
        elif code == 1:
            self.grid[next_pos] = FLOOR
            self.pos = next_pos
            self.update_targets()
        elif code == 2:
            self.pos = next_pos
            self.update_targets()
            self.oxygen_system = next_pos

        return []

    def explore_map(self):
        input_value = get_input()
        self.p = IntProcessor(input_value)

        self.p.get_input = self.get_input
        self.p.process_output = self.process_output
        self.p.run()

    def get_oxygen_system_path(self):
        min_path = self.get_path((W, W), self.oxygen_system)
        return len(min_path) - 1

    def fill_oxygen(self):
        missing = {
            pos
            for pos, v in self.grid
            if v == FLOOR
        }
        nodes = {self.oxygen_system}

        minutes = 0
        while missing:
            new_nodes = set()
            for node in nodes:
                for direction in GRID_DIRECTIONS:
                    node2 = apply_direction(node, direction)
                    if node2 in missing:
                        new_nodes.add(node2)
                        missing.remove(node2)

            nodes = new_nodes
            minutes += 1

        return minutes



s = System()
s.explore_map()

s.get_oxygen_system_path() | debug('Star 1') | eq(270)

s.fill_oxygen() | debug('Star 2') | eq(364)
