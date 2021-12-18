import _md5
import atexit
import bisect
import functools
import hashlib
import heapq
import itertools
import json
import math
import multiprocess as mp
import numpy as np
import operator
import os
import re
import requests
import string
import subprocess
import sympy
import sys
import textwrap
import traceback
import webbrowser
from bs4 import BeautifulSoup
from collections import defaultdict, deque, namedtuple, Counter
from copy import deepcopy
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from termcolor import colored


PROCESSES = 8
IN_CI = 'CI' in os.environ

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

def bit_count(value):
    bits = 0
    for i in range(10000):
        bit = 1 << i
        if value < bit:
            break
        if value & bit:
            bits += 1
    return bits

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

def zlist(N):
    return [0 for i in range(N)]

def heapify(lst):
    heapq.heapify(lst)
    return lst

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
            message = f"""
            {get_frame_location()}
            - {green('PASS')}: [{value}]
            """
            print_message(message)
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
        if IN_CI:
            raise OSError('No clipboard() in CI')

        value = f'{value}'
        p = subprocess.Popen(
            ['pbcopy', 'w'],
            stdin=subprocess.PIPE,
            close_fds=True,
        )
        p.communicate(input=value.encode('utf-8'))
        return value

class Submit:
    def __init__(self, star):
        self.star = star

        # Fetch year and day from problem filename
        frame = get_test_frame()

        year = os.path.basename(
            os.path.dirname(frame.filename)
        )
        filename = os.path.basename(frame.filename)
        day, _ = os.path.splitext(filename)
        day = int(day)

        self.year = year
        self.day = day

    def __ror__(self, answer):
        try:
            return self.unsafe_ror(answer)
        except Exception as e:
            print('\n\nError submitting:')
            print(e)
            print('\n\n')
            print(red('Failed to submit, copying to clipboard instead'))
            return answer | Clipboard()

    def unsafe_ror(self, answer):
        if IN_CI:
            raise OSError('No submit() in CI')

        if answer is None:
            print(yellow('Skipping [None] answer\n'))
            return answer

        star = '⭐' * self.star

        print('\n\n')
        print(f'Submit answer for {star} ?', yellow('y/n'))
        print(f'  -> [{blue(str(answer))}]\n\n')

        response = input()
        if response.lower() != 'y':
            print(yellow('Not submitting'))
            return

        html = self.submit_answer(answer)
        self.print_clean_response(html)
        print()

        # Store correct answer in the clipboard
        answer | Clipboard()

    def submit_answer(self, answer):
        aoc_dir = os.path.join(
            os.path.dirname(__file__), 'advent_of_code',
        )
        session_filename = os.path.abspath(
            os.path.join(aoc_dir, '.session')
        )
        with open(session_filename, 'r') as fd:
            session = fd.read().strip()

        url = f'https://adventofcode.com/{self.year}/day/{self.day}/answer'
        payload = {
            'level': self.star,
            'answer': str(answer),
        }
        headers = {
            'X-MAS': 'hi-eric-thank-you-for-making-aoc',
            'cookie': f'session={session}',
        }

        req = requests.post(url, headers=headers, data=payload)
        return req.text

    def print_clean_response(self, html):
        s = BeautifulSoup(html, 'html.parser')
        article = [
            article
            for main in s.find_all('main')
            for article in main.find_all('article')
        ][0]

        response = article.get_text()

        if "That's the right answer!" in response:
            print(green("That's the right answer!"))

            match = re.search('You achieved rank (\d+)', response)
            if match is not None:
                rank = int(match.groups()[0])
                points = 101 - rank
                print(green(f'Leaderboard: {rank}'), blue(f'({points})'))
            else:
                match = re.search('You got rank (\d+)', response)
                if match is not None:
                    rank = int(match.groups()[0])
                    print(blue(f'Rank: {rank}'))

            # Quick-open part 2
            if self.star == 1:
                url = f'https://adventofcode.com/{self.year}/day/{self.day}#part2'
                webbrowser.open(url)

            return

        if "That's not the right answer" in response:
            output = red("That's not the right answer")

            if 'answer is too high' in response:
                output += f' ({blue("Too high")})'
            elif 'answer is too low' in response:
                output += f' ({blue("Too low")})'

            print(output)
            return

        if "You gave an answer too recently" in response:
            match = re.search('You have (\d+)s left to wait.', response)
            if match is not None:
                wait_time = match.groups()[0]
            else:
                wait_time = '???'

            print(blue('You gave an answer too recently:'), yellow(f'Wait {wait_time}s'))
            return

        print(yellow(response))

def debug(header=''):
    return Debug(header)

def eq(expected_result):
    return Eq(expected_result)

def clipboard():
    return Clipboard()

def submit(star):
    return Submit(star)

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

def pos_distance(a, b):
    return sum(
        abs(ai + bi)
        for ai, bi in zip(a, b)
    )

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

    @staticmethod
    def from_points(points, *, set_value='#', unset_value='.'):
        max_x = max(x for x, y in points)
        min_x = min(x for x, y in points)
        max_y = max(y for x, y in points)
        min_y = min(y for x, y in points)
        grid = Grid([
            [unset_value for x in range(min_x, max_x + 1)]
            for y in range(min_y, max_y + 1)
        ])
        for pos in points:
            grid[pos] = set_value
        return grid

    @property
    def entry_count(self):
        return self.width * self.height

    @property
    def center(self):
        return (self.width // 2, self.width // 2)

    def copy(self):
        return Grid([
            [c for c in row]
            for row in self.grid
        ])

    def replace(self, v1, v2):
        for pos, v in self:
            if v == v1:
                self[pos] = v2

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

    def __contains__(self, pos):
        (x, y) = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def __max__(self):
        return max(
            x
            for row in self.grid
            for x in row
        )

    def __min__(self):
        return min(
            x
            for row in self.grid
            for x in row
        )

    def count(self, value):
        return len([
            1
            for _, v in self
            if v == value
        ])

    def apply_direction(self, pos, direction):
        next_pos = apply_direction(pos, direction)

        if next_pos in self:
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
            if (n := apply_direction(pos, direction)) in self
        ]

    def print(self, use_padding=None):
        max_digits = len(f'{self.width}')

        if use_padding is None:
            has_padding = self.width <= 80
        else:
            has_padding = use_padding

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

def md5(s):
    return _md5.md5(str.encode(s)).hexdigest()

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

def int_or(v, default):
    try:
        return int(v)
    except:
        return default
