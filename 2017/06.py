from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

class Problem:
    def __init__(self, problem, lines):
        self.problem = problem
        self.values = [int(x) for x in lines[0].split()]

    def run(self):
        values = self.values
        blocks = len(values)

        cache = {}
        while True:
            key = tuple(values)
            if key in cache:
                loop = len(cache)
                if self.problem == 1:
                    return loop
                else:
                    return loop - cache[key]
            cache[key] = len(cache)

            max_value = max(values)
            idx = values.index(max_value)
            values[idx] = 0

            common = max_value // blocks
            remainder = max_value % blocks
            for i in range(blocks):
                idx2 = (idx + i + 1) % blocks
                new_blocks = common
                if remainder and i < remainder:
                    new_blocks += 1
                values[idx2] += new_blocks

        return len(cache)

def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

example1 = multiline_lines(r"""
0 2 7 0
""")

run(example1) | eq(5)

run(input_lines) | debug('Star 1') | eq(5042)

run2(example1) | eq(4)

run2(input_lines) | debug('Star 2') | clipboard()
