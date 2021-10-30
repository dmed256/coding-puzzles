import os
import textwrap
import traceback
from termcolor import colored


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


#---[ Utils ]---------------------------
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
