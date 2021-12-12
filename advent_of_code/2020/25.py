from repo_utils import *

input_value = get_input()
input_lines = get_input_lines()

MOD_VALUE = 20201227

class Problem:
    def __init__(self, problem, lines):
        self.problem = problem
        self.public_keys = [int(x) for x in lines]

    def get_loop(self, value):
        value = value % MOD_VALUE

        v = 1
        for loop in range(1, MOD_VALUE):
            v = (v * 7) % MOD_VALUE
            if v == value:
                break

        return loop

    def calculate_value(self, loop, subject_number):
        value = 1
        for i in range(loop):
            value = (value * subject_number) % MOD_VALUE
        return value

    def run(self):
        loop0 = self.get_loop(self.public_keys[0])
        loop1 = self.get_loop(self.public_keys[1])

        key1 = self.calculate_value(loop0, self.public_keys[1])
        key2 = self.calculate_value(loop1, self.public_keys[0])
        assert key1 == key2
        return key1

def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

example1 = multiline_lines(r"""
5764801
17807724
""")

run(example1) | eq(14897079)
run(input_lines) | debug('Star 1') | eq(9177528)
