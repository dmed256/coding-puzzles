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

def toc(header):
    end = datetime.now()
    start = timestamps.pop()

    seconds_taken = int((end - start).total_seconds())
    minutes_taken = seconds_taken // 60
    seconds_taken = seconds_taken % 60
    time_taken = yellow(f'{minutes_taken}m{seconds_taken:02d}s')

    print(blue(header))
    print(f'  - Time taken: {time_taken}')


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
