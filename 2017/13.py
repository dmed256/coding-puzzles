from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

class Problem:
    def __init__(self, problem, lines):
        self.problem = problem

        layers = {}
        for line in lines:
            [layer, depth] = line.split(': ')
            layers[int(layer)] = int(depth)

        self.layers = layers

    def run(self):
        layers = self.layers
        cycles = {
            layer: (depth, 2 * (depth - 1))
            for layer, depth in layers.items()
        }

        if self.problem == 1:
            severity = 0
            for layer, (depth, cycle) in cycles.items():
                packet = layer % cycle
                if packet == 0:
                    severity += layer * depth

            return severity

        delay = 1
        while True:
            safe = True
            for layer, (_, cycle) in cycles.items():
                if not (layer + delay) % cycle:
                    safe = False
                    break

            if safe:
                return delay

            delay += 1

def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

example1 = multiline_lines(r"""
0: 3
1: 2
4: 4
6: 4
""")

run(example1) | eq(24)

run(input_lines) | debug('Star 1') | eq(1632)

run2(example1) | eq(10)

run2(input_lines) | debug('Star 2') | eq(3834136)
