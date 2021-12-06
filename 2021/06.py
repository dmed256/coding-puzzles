from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

class Problem:
    def __init__(self, problem, lines):
        self.problem = problem
        self.values = [int(x) for x in lines[0].split(',')]

    def run(self):
        fish = {
            i: 0
            for i in range(10)
        }
        for value in self.values:
            fish[value] += 1

        days = 80 if self.problem == 1 else 256

        for i in range(days):
            next_fish = fish[0]
            for j in range(1, 10):
                if j in fish:
                    fish[j - 1] = fish[j]
            fish[6] += next_fish
            fish[8] += next_fish

        return sum(x for x in fish.values())

def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

example1 = multiline_lines(r"""
3,4,3,1,2
""")

run(example1) | eq(5934)

run(input_lines) | debug('Star 1') | eq(388739)

run2(example1) | eq(26984457539)

run2(input_lines) | debug('Star 2') | eq(1741362314973)
