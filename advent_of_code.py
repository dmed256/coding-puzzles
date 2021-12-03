import atexit
import itertools
import multiprocess as mp
import numpy as np
import operator
import os
import re
import subprocess
import sympy
import sys
import textwrap
import traceback
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from termcolor import colored


PROCESSES = 8

#---[ Input ]---------------------------
def multiline_lines(s):
    lines = [
        line
        for line in s.splitlines()
    ]
    if not lines[0]:
        lines = lines[1:]
    if not lines[-1]:
        lines = lines[:-1]
    return lines

def multiline_input(s):
    return '\n'.join(multiline_lines(s))

def get_input_lines():
    filename = sys.argv[0]
    input_filename = f'{os.path.splitext(filename)[0]}_input'

    with open(input_filename, 'r') as fd:
        lines = fd.readlines()

    return [
        line.replace('\n', '')
        for line in lines
    ]

def get_input():
    return '\n'.join(get_input_lines())


#---[ Output ]--------------------------

#---[ Timing ]--------------------------
timestamps = []

def now():
    return datetime.now()

def tic():
    timestamps.append(now())

def toc(header=''):
    end = now()
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
# TODO:
# - arg_min with key
# - arg_max with key
# - reduction

def lget(lst, index, default=None):
    if index >= 0 and index >= len(lst):
        return default
    if index < 0 and -index > len(lst):
        return default
    return lst[index]

def safe_min(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return min(a, b)

def safe_max(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return max(a, b)

def extract_ints(value):
    return [int(v) for v in re.findall(r'\d+', value)]

def split_comma_ints(value, delimiter=','):
    return [
        int(x.strip())
        for x in value.split(delimiter)
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

def get_bits(value):
    bits = []
    bit = 0
    bit_value = 1
    while bit_value <= value:
        if value & bit_value:
            bits.append((bit, bit_value))
        bit += 1
        bit_value *= 2
    return bits

def format_bits(value):
    bits = []
    while value:
        bits.append(value % 2)
        value = value // 2

    bits = (bits or [0])[::-1]

    return ''.join([str(b) for b in bits])

def invrange(a, b=None):
    if b is None:
        return range(a - 1, -1, -1)
    return range(b - 1, a - 1, -1)

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

test_errors = 0

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
        return value

class Eq:
    def __init__(self, expected_value):
        self.expected_value = expected_value

    def __ror__(self, value):
        if value == self.expected_value:
            return value

        global test_errors
        test_errors += 1

        output = red(f'{value}')
        expected_output = green(f'{self.expected_value}')

        message = f"""
        {get_frame_location()}
          - OUTPUT:   [{output}]
          - EXPECTED: [{expected_output}]
        """

        print_message(message)
        return value

class Clipboard:
    def __ror__(self, value):
        value = f'{value}'
        p = subprocess.Popen(
            ['pbcopy', 'w'],
            stdin=subprocess.PIPE,
            close_fds=True,
        )
        p.communicate(input=value.encode('utf-8'))

def debug(header=''):
    return Debug(header)

def eq(expected_result):
    return Eq(expected_result)

def clipboard():
    return Clipboard()

def assert_tests_passed():
    global test_errors
    if test_errors:
        print(red(f'TESTS FAILED: {test_errors}'))
        os._exit(1)

atexit.register(assert_tests_passed)

#---[ Constants ]-----------------------
# Grid directions
UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [DOWN, LEFT, RIGHT, UP]

GRID_UP = (0, -1)
GRID_DOWN = (0, 1)
GRID_LEFT = (-1, 0)
GRID_RIGHT = (1, 0)
GRID_DIRECTIONS = [
    GRID_DOWN,
    GRID_LEFT,
    GRID_RIGHT,
    GRID_UP,
]

NORTH = UP
SOUTH = DOWN
WEST = LEFT
EAST = RIGHT

SOUTHWEST = (-1, -1)
SOUTHEAST = (1, -1)
NORTHWEST = (-1, 1)
NORTHEAST = (1, 1)

DIAG_DIRECTIONS = [
    SOUTH,
    NORTH,
    WEST,
    EAST,
    SOUTHWEST,
    SOUTHEAST,
    NORTHWEST,
    NORTHEAST,
]

GRID_CLOCKWISE = {
    GRID_UP: GRID_RIGHT,
    GRID_RIGHT: GRID_DOWN,
    GRID_DOWN: GRID_LEFT,
    GRID_LEFT: GRID_UP,
}

GRID_COUNTER_CLOCKWISE = {
    GRID_UP: GRID_LEFT,
    GRID_LEFT: GRID_DOWN,
    GRID_DOWN: GRID_RIGHT,
    GRID_RIGHT: GRID_UP,
}

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

ASCII_TO_DIRECTION = {
    '^': UP,
    'v': DOWN,
    '<': LEFT,
    '>': RIGHT,
}

ASCII_TO_GRID_DIRECTION = {
    '^': GRID_UP,
    'v': GRID_DOWN,
    '<': GRID_LEFT,
    '>': GRID_RIGHT,
}

DIRECTION_TO_ASCII = {
    UP: '^',
    DOWN: 'v',
    LEFT: '<',
    RIGHT: '>',
}

GRID_DIRECTION_TO_ASCII = {
    UP: '^',
    DOWN: 'v',
    LEFT: '<',
    RIGHT: '>',
}

#---[ Grid ]----------------------------
def add_tuples(a, b):
    return tuple(map(operator.add, a, b))

def apply_direction(pos, direction):
    return add_tuples(pos, direction)

def pos_distance(pos):
    return abs(pos[0]) + abs(pos[1])

class Grid:
    def __init__(self, grid, *, default_value=None):
        self.width = max(len(row) for row in grid)

        def build_row(row):
            padding = [default_value] * (self.width - len(row))
            return [v for v in row] + padding

        self.grid = [
            build_row(row)
            for row in grid
        ]
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
                yield (x, y), self.grid[y][x]

    def in_grid(self, pos):
        (x, y) = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def apply_direction(self, pos, direction):
        next_pos = apply_direction(pos, direction)

        if self.in_grid(next_pos):
            return next_pos

        return None

    def find_all(self, value):
        return [
            pos
            for pos, c in self
            if c == value
        ]

    def first(self, value):
        values = self.find_all(value)
        if values:
            return values[0]
        return None

    def neighbors(self, pos, directions=GRID_DIRECTIONS):
        return [
            n
            for direction in directions
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
            output += padding_char.join([
                str(v) for v in row
            ])
            output += ' │\n'
        output += padding[:-1] + '└' + ('─' * (x_axis_length + 2)) + '┘\n'
        print(output)

#---[ Graph ]---------------------------
class Graph:
    class Type(Enum):
        NOTHING = 0
        WALL = 1
        OBJECT = 2

    def __init__(self, grid, *, start_pos, get_type):
        self.grid = grid
        self.neighbors = {}

        # value -> Graph.Type
        self.get_type = get_type

        # Explore map
        if isinstance(start_pos, list):
            nodes = [*start_pos]
        else:
            nodes = [start_pos]

        explored = set(nodes)
        while nodes:
            new_nodes = set()
            for node in nodes:
                neighbors = [
                    n
                    for n in self.grid.neighbors(node)
                    if self.get_pos_type(n) != Graph.Type.WALL
                ]
                self.neighbors[node] = neighbors
                new_nodes.update(neighbors)
            nodes = new_nodes - explored
            explored.update(nodes)

        self.pos_to_object = {
            (x, y): v
            for (x, y) in explored
            if (v := self.grid[(x, y)])
            and self.get_type(v) == Graph.Type.OBJECT
        }
        self.object_to_pos = {}
        for pos, v in self.pos_to_object.items():
            positions = self.object_to_pos.get(v, [])
            self.object_to_pos[v] = positions + [pos]

        self.objects = set(self.pos_to_object.keys())

    def get_pos_type(self, pos):
        return self.get_type(self.grid[pos])

    def bfs(self, pos):
        nodes = set(self.neighbors.get(pos, []))
        explored = {pos}
        while nodes:
            next_nodes = set()
            for n in nodes:
                yield n
                next_nodes.update(
                    self.neighbors.get(n, [])
                )
            nodes = next_nodes - explored
            explored.update(nodes)

    def find_paths(self, start, targets):
        targets = set(targets)

        prev_nodes = { start: None }

        nodes = {start}
        explored = {start}
        while nodes:
            new_nodes = set()
            for node in nodes:
                neighbors = [
                    neighbor
                    for neighbor in self.neighbors[node]
                    if neighbor not in prev_nodes
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

#---[ Math ]----------------------------

# Solve using "Extended Euclidean" (assumming a and M are co-prime)
#         x = a^-1      (mod M)
#        ax = 1         (mod M)
#   ax + My = 1
#   ax + My = gcd(a, M)
def inverse_mod(a, M):
    prev_x, x = 1, 0
    prev_r, r = a, M

    while prev_r > 1:
        # a = quotient*M + r
        quotient = prev_r // r
        (prev_r, r) = (r, prev_r - (quotient * r))
        (prev_x, x) = (x, prev_x - (quotient * x))

    return prev_x % M

def get_subgroups(values):
    for i in range(len(values)):
        for combination in itertools.combinations(values, i):
            yield combination

def mult(values):
    v = 1
    for value in values:
        v *= value
    return v

def get_primes(N):
    nth_prime = sympy.prime(N)
    return list(sympy.primerange(nth_prime + 1))

def get_primes_before(N):
    return list(sympy.primerange(N))

def to_binary(num):
    value = ''
    for i in range(10000):
        if value & (1 << i):
            value += '1'
        else:
            value += '0'
        value = value << 1
        if not value:
            break

    return value[::-1]

def from_binary(s):
    value = 0
    for i, bit in enumerate(s[::-1]):
        if bit == '1':
            value += 1 << i
    return value
