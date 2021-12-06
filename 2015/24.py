from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

class Problem:
    def __init__(self, problem, lines):
        self.problem = problem
        self.values = [int(x) for x in lines]

    def run(self):
        count = len(self.values)
        group_weight = sum(self.values) // 3

        sorted_values = sorted(self.values, reverse=True)
        queue = [([x], x, i) for i, x in enumerate(sorted_values)]
        cache = {}

        min_qe = None
        min_length = count
        while queue:
            values, weight, max_index = queue.pop(0)

            if len(values) >= min_length:
                break

            if weight == group_weight:
                min_qe = safe_min(min_qe, mult(values))
                min_length = len(values)

            for vi, v in enumerate(sorted_values[max_index + 1:]):
                vi = max_index + 1 + vi
                w2 = weight + v
                if w2 <= group_weight:
                    queue.append(({*values, v}, w2, vi))

        return min_qe

def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

example1 = multiline_lines(r"""
1
2
3
4
5
7
8
9
10
11
""")

run(example1) | eq(99)

run(input_lines) | debug('Star 1') | clipboard()

# run2(example1) | eq()

# run2(input_lines) | debug('Star 2') | clipboard()
