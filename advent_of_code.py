import os
import multiprocess as mp
import numpy as np
import textwrap
import traceback
from enum import Enum
from datetime import datetime
from termcolor import colored


PROCESSES = 8

#---[ Input ]---------------------------
def multiline_lines(s):
    return [
        line.strip()
        for line in s.splitlines()
        if line.strip()
    ]

def multiline_input(s):
    return '\n'.join(multiline_lines(s))

def get_input_lines():
    frame = traceback.extract_stack()[0]
    filename = os.path.basename(frame.filename)

    input_filename = f'{os.path.splitext(filename)[0]}_input'

    with open(input_filename, 'r') as fd:
        lines = fd.readlines()

    return [
        line.replace('\n', '')
        for line in lines
    ]

def get_input():
    return '\n'.join(get_input_lines())


#---[ Timing ]--------------------------
timestamps = []

def tic():
    timestamps.append(datetime.now())

def toc(header=''):
    end = datetime.now()
    start = timestamps.pop()

    time_taken = (end - start).total_seconds()
    minutes_taken = int(time_taken) // 60
    seconds_taken = time_taken % 60
    if seconds_taken < 10:
        seconds_taken = f'0{seconds_taken:.3f}'
    else:
        seconds_taken = f'{seconds_taken:.3f}'

    time_taken = yellow(
        f'Time taken: {minutes_taken}m{seconds_taken}s'
    )

    if header:
        print(blue(header))
        print(f'  - {time_taken}')
    else:
        print(time_taken)
    print()


#---[ Parallel ]------------------------
class PmapArgType(Enum):
    VALUE = 1
    NUMPY_ARRAY = 2

def encode_pmap_arg(key, i, arg):
    if type(arg) != np.ndarray:
        return (PmapArgType.VALUE, i, arg)

    filename = f'{key}_{i}.npy'
    with open(filename, 'wb') as f:
        np.save(f, arg)
    return (PmapArgType.NUMPY_ARRAY, i, filename)

def decode_pmap_arg(arg):
    (arg_type, i, value) = arg
    if arg_type == PmapArgType.VALUE:
        return value

    with open(value, 'rb') as f:
        value = np.load(f)
    return value

def encode_pmap_args(key, args):
    return [
        encode_pmap_arg(key, i, arg)
        for i, arg in enumerate(args)
    ]

def decode_pmap_args(args):
    return [
        decode_pmap_arg(arg)
        for arg in args
    ]

def clean_pmap_args(args):
    numpy_files = [
        value
        for (arg_type, i, value) in args
        if arg_type == PmapArgType.NUMPY_ARRAY
    ]
    for numpy_file in numpy_files:
        os.remove(numpy_file)

def pmap(key, fn, args):
    result_key = f'{key}_result'

    if not hasattr(pmap, 'pool'):
        pmap.pool = mp.Pool(PROCESSES)

    encoded_args = encode_pmap_args(key, args)

    def fn_wrapper(i):
        args = decode_pmap_args(encoded_args)
        value = fn(PROCESSES, i, *args)
        return encode_pmap_arg(result_key, i, value)

    encoded_results = pmap.pool.map(fn_wrapper, range(PROCESSES), 1)
    results = [
        decode_pmap_arg(encoded_result)
        for encoded_result in encoded_results
    ]

    clean_pmap_args(encoded_args)
    clean_pmap_args(encoded_results)

    return results


#---[ Utils ]---------------------------
def lget(lst, index):
    if index < len(lst):
        return lst[index]
    return None

def split_comma_ints(value):
    return [
        int(x.strip())
        for x in value.split(',')
        if x
    ]

def shortest_list(lists):
    lists = [
        lst
        for lst in lists
        if lst is not None
    ]
    if lists:
        return min(lists, key=lambda x: len(x))
    return None

def longest_list(lists):
    lists = [
        lst
        for lst in lists
        if lst is not None
    ]
    if lists:
        return max(lists, key=lambda x: len(x))
    return None


#---[ Colors ]--------------------------
def blue(value):
    return colored(value, 'blue')

def green(value):
    return colored(value, 'green')

def red(value):
    return colored(value, 'red')

def yellow(value):
    return colored(value, 'yellow')


#---[ Testing ]-------------------------
def get_test_frame():
    return traceback.extract_stack()[0]

def get_frame_location(frame=None):
    frame = frame or get_test_frame()

    filename = os.path.basename(frame.filename)
    location = f'{filename}:{frame.lineno}'
    line = frame.line

    return f'{blue(location)}  {yellow(line)}'

def print_message(message):
    print('')
    print(textwrap.dedent(message).strip())
    print('')

class Testable:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        return Test(
            self.func(*args, **kwargs),
            get_test_frame(),
        )


class Test:
    def __init__(self, result, frame):
        self.result = result
        self.frame = frame

    @property
    def value(self):
        return self.result

    def get_location(self):
        return get_frame_location(self.frame)

    def debug(self, header=''):
        output = blue(f'{self.result}')

        message = f"""
        {blue(header)}
        {self.get_location()}
          -> [{output}]
        """

        print_message(message)

    def should_be(self, expected_result):
        if self.result == expected_result:
            return

        output = red(f'{self.result}')
        expected_output = green(f'{expected_result}')

        message = f"""
        {self.get_location()}
          - OUTPUT:   [{output}]
          - EXPECTED: [{expected_output}]
        """

        print_message(message)

# DEPRECATED
def testable(func):
    return Testable(func)

class Debug:
    def __init__(self, header):
        self.header = header

    def __ror__(self, value):
        output = blue(f'{value}')

        message = f"""
        {self.header}
        {get_frame_location()}
          -> [{output}]
        """

        print_message(message)

class ShouldBe:
    def __init__(self, expected_value):
        self.expected_value = expected_value

    def __ror__(self, value):
        if value == self.expected_value:
            return

        output = red(f'{value}')
        expected_output = green(f'{self.expected_value}')

        message = f"""
        {get_frame_location()}
          - OUTPUT:   [{output}]
          - EXPECTED: [{expected_output}]
        """

        print_message(message)

def debug(header=''):
    return Debug(header)

# DEPRECATED
def should_be(expected_result):
    return ShouldBe(expected_result)

def eq(expected_result):
    return ShouldBe(expected_result)


#---[ Constants ]-----------------------
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [DOWN, LEFT, RIGHT, UP]

CLOCKWISE = {
    UP: RIGHT,
    RIGHT: DOWN,
    DOWN: LEFT,
    LEFT: UP,
}

COUNTER_CLOCKWISE = {
    UP: LEFT,
    LEFT: DOWN,
    DOWN: RIGHT,
    RIGHT: UP,
}

# (0, 0) is usually top-left of the grid
ASCII_TO_DIRECTION = {
    '^': UP,
    'v': DOWN,
    '<': LEFT,
    '>': RIGHT,
}

DIRECTION_TO_ASCII = {
    UP: '^',
    DOWN: 'v',
    LEFT: '<',
    RIGHT: '>',
}

def apply_direction(pos, direction):
    (x, y) = pos
    (dx, dy) = direction
    return (x + dx, y + dy)

class Grid:
    def __init__(self, grid):
        self.grid = [
            [v for v in row]
            for row in grid
        ]
        self.width = len(self.grid[0])
        self.height = len(self.grid)

    def copy(self):
        return Grid(self.grid.copy())

    def __getitem__(self, pos):
        (x, y) = pos
        return self.grid[y][x]

    def __setitem__(self, pos, value):
        (x, y) = pos
        self.grid[y][x] = value
        return value

    def __iter__(self):
        for y in range(self.height):
            for x in range(self.width):
                yield (x, y, self.grid[y][x])

    def in_grid(self, pos):
        (x, y) = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def apply_direction(self, pos, direction):
        next_pos = apply_direction(pos, direction)

        if in_grid(next_pos):
            return next_pos

        return None

    def find_all(self, value):
        return [
            (x, y)
            for (x, y, c) in self
            if c == value
        ]

    def first(self, value):
        values = self.find_all(value)
        if values:
            return values[0]
        return None

    def neighbors(self, pos):
        return [
            n
            for direction in DIRECTIONS
            if self.in_grid(n := apply_direction(pos, direction))
        ]

    def print(self):
        max_digits = len(f'{self.width}')
        has_padding = self.width <= 80
        padding_char = '  ' if has_padding else ''

        def get_digit_value(value, digit):
            pow10 = 10**digit
            d = (value // pow10) % 10

            if d or value >= pow10:
                return d
            if value == 0 and digit == 0 :
                return 0

            return ' '

        padding = '     '
        x_axis = [
            padding_char.join([
                f'{get_digit_value(x, digit)}'
                for x in range(self.width)
            ])
            for digit in range(max_digits)
        ][::-1]
        x_axis_length = len(x_axis[0])

        output = ''
        for x in x_axis:
            output += padding + ' ' + x + '\n'

        output += padding[:-1] + '┌' + ('─' * (x_axis_length + 2)) + '┐\n'
        for (y, row) in enumerate(self.grid):
            output += f'{y:>3} │ '
            output += padding_char.join(row)
            output += ' │\n'
        output += padding[:-1] + '└' + ('─' * (x_axis_length + 2)) + '┘\n'
        print(output)

class Graph:
    class Type(Enum):
        NOTHING = 0
        WALL = 1
        OBJECT = 2

    def __init__(self, grid, *, start_pos, get_type):
        self.grid = grid
        self.graph = {}

        # value -> Graph.Type
        self.get_type = get_type

        # Explore map
        nodes = [start_pos]
        explored = set([start_pos])
        while nodes:
            new_nodes = set()
            for node in nodes:
                neighbors = [
                    n
                    for n in self.grid.neighbors(node)
                    if self.get_pos_type(n) != Graph.Type.WALL
                ]
                self.graph[node] = neighbors
                new_nodes.update(neighbors)
            nodes = new_nodes - explored
            explored.update(nodes)

        self.pos_to_object = {
            (x, y): v
            for (x, y) in explored
            if (v := self.grid[(x, y)])
            and self.get_type(v) == Graph.Type.OBJECT
        }

    def get_pos_type(self, pos):
        return self.get_type(self.grid[pos])

    def find_paths(self, start, targets, obstacles=None):
        targets = set(targets)
        obstacles = obstacles or set()

        prev_nodes = { start: None }
        for obstacle in obstacles:
            prev_nodes[obstacle] = None

        nodes = set([start])
        explored = set([start])
        while nodes:
            new_nodes = set()
            for node in nodes:
                neighbors = [
                    neighbor
                    for neighbor in self.graph[node]
                    if neighbor not in prev_nodes
                    and neighbor not in obstacles
                ]

                new_nodes.update(neighbors)
                explored.update(neighbors)

                for n in neighbors:
                    prev_nodes[n] = node

            # We've found paths for all targets
            if targets <= explored:
                break

            nodes = new_nodes

        def traverse_back_path(target):
            if target not in prev_nodes:
                return None
            node = target
            path = []
            while node != start:
                path.append(node)
                node = prev_nodes[node]
            return path[::-1]

        return [
            path
            for target in targets
            if (path := traverse_back_path(target))
        ]


    def find_path(self, start, end, obstacles=None):
        if start == end:
            return []

        explored = set(start)
        if obstacles:
            explored.update(obstacles)

        paths = [[start]]
        while paths:
            paths = [
                [*path, neighbor]
                for path in paths
                for neighbor in self.graph[path[-1]]
                if neighbor not in explored
            ]
            new_nodes = [
                path[-1]
                for path in paths
            ]
            explored.update(new_nodes)
            if end in explored:
                return [
                    # Remove start from the path
                    path[1:]
                    for path in paths
                    if path[-1] == end
                ][0]

        return None
