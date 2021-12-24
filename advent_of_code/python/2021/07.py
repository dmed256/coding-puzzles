from repo_utils import *

input_value = get_input()
input_lines = get_input_lines()

class Problem:
    def __init__(self, problem, lines):
        self.problem = problem
        self.values = [int(x) for x in lines[0].split(',')]

    def run(self):
        values = self.values

        min_fuel = None
        for dest in range(max(self.values)):
            if self.problem == 1:
                cost = sum(
                    abs(dest - x)
                    for x in self.values
                )
            else:
                cost = sum(
                    (abs(dest - x) * (abs(dest - x) + 1)) // 2
                    for x in self.values
                )
            min_fuel = safe_min(min_fuel, cost)

        return min_fuel

def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

example1 = multiline_lines(r"""
16,1,2,0,4,2,7,1,2,14
""")

run(example1) | eq(37)

run(input_lines) | debug('Star 1') | eq(337488)

run2(example1) | eq(168)

run2(input_lines) | debug('Star 2') | eq(89647695)
