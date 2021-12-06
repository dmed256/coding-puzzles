from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

class Problem:
    def __init__(self, problem, lines):
        self.problem = problem
        self.values = [int(x) for x in lines]

    def run(self):
        values = self.values

        ptr = 0
        steps = 0
        while 0 <= ptr < len(values):
            steps += 1

            offset = values[ptr]
            ptr2 = ptr + offset

            if self.problem == 2 and offset >= 3:
                values[ptr] -= 1
            else:
                values[ptr] += 1

            ptr = ptr2

        return steps

def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

example1 = multiline_lines(r"""
0
3
0
1
-3
""")

run(example1) | eq(5)

run(input_lines) | debug('Star 1') | eq(394829)

run2(example1) | eq(10)

run2(input_lines) | debug('Star 2') | eq(31150702)
