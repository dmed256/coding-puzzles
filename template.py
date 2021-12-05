from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

class Problem:
    def __init__(self, problem, lines):
        self.problem = problem

    def run(self):
        return None

def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

example1 = multiline_lines(r"""
""")

run(example1) | eq()

run(input_lines) | debug('Star 1') | clipboard()

# run2(example1) | eq()

# run2(input_lines) | debug('Star 2') | clipboard()
