import re
import itertools
from termcolor import colored
from advent_of_code import *
from int_processor import *

class Problem:
    def __init__(self):
        self.last_signal = None

    def get_input(self, i):
        def get_amp_input():
            if self.p_inputs[i]:
                return self.p_inputs[i].pop(0)
            return PAUSE

        return get_amp_input

    def process_output(self, i):
        def process_amp_output(output):
            [value] = output
            self.p_inputs[(i + 1) % 5].append(value)

            if i == 4:
                self.last_signal = value

            return []

        return process_amp_output

    def is_done(self):
        return 5 == sum([
            p.is_done
            for p in self.processors
        ])

    def run(self, int_code, problem, phase_settings):
        self.processors = [
            IntProcessor(int_code)
            for i in range(5)
        ]
        for i, p in enumerate(self.processors):
            p.get_input = self.get_input(i)
            p.process_output = self.process_output(i)

        self.p_inputs = [
            [phase_setting]
            for phase_setting in phase_settings
        ]
        self.p_inputs[0].append(0)

        for p in self.processors:
            p.run()

        if problem == 1:
            return self.last_signal

        while not self.is_done():
            for i, p in enumerate(self.processors):
                if p.is_done:
                    continue

                p_inputs = self.p_inputs[i]
                if not p_inputs:
                    continue

                p.unpause(p_inputs.pop(0))

        return self.last_signal

def run(code, problem):
    int_code = split_comma_ints(code)
    sequence = (
        [0, 1, 2, 3, 4]
        if problem == 1 else
        [5, 6, 7, 8, 9]
    )

    max_signal = 0
    for phase_settings in itertools.permutations(sequence):
        p = Problem()
        signal = p.run(int_code, problem, phase_settings)
        max_signal = max(max_signal, signal)

    return max_signal

example1 = multiline_input(r"""
3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0
""")
example2 = multiline_input(r"""
3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0
""")
example3 = multiline_input(r"""
3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0
""")

run(example1, 1) | eq(43210)
run(example2, 1) | eq(54321)
run(example3, 1) | eq(65210)

input_value = get_input()
run(input_value, 1) | debug('Star 1') | eq(880726)

example1 = multiline_input("""
3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
""")
example2 = multiline_input("""
3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10
""")

run(example1, 2) | eq(139629729)
run(example2, 2) | eq(18216)
run(input_value, 2) | debug('Star 2') | eq(4931744)
