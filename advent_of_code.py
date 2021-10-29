import os
import textwrap
import traceback
from termcolor import colored


# Input
def multiline_lines(s):
    return [
        line.strip()
        for line in s.splitlines()
        if line.strip()
    ]

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


# Colors
def blue(value):
    return colored(value, 'blue')

def green(value):
    return colored(value, 'green')

def red(value):
    return colored(value, 'red')

def yellow(value):
    return colored(value, 'yellow')


# Testing
class Testable:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        result = self.func(*args, **kwargs)
        frame = traceback.extract_stack()[0]

        return Test(result, frame)


class Test:
    def __init__(self, result, frame):
        self.result = result
        self.frame = frame

    @property
    def value(self):
        return self.result

    def get_location(self):
        filename = os.path.basename(self.frame.filename)
        location = f'{filename}:{self.frame.lineno}'
        line = self.frame.line

        return f'{blue(location)}  {yellow(line)}'

    def print_message(self, message):
        print('')
        print(textwrap.dedent(message).strip())
        print('')


    def debug(self, header=''):
        output = blue(f'{self.result}')

        message = f"""
        {blue(header)}
        {self.get_location()}
          -> [{output}]
        """

        self.print_message(message)

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

        self.print_message(message)


def testable(func):
    return Testable(func)
