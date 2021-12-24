from repo_utils import *

class Problem:
    def __init__(self, problem, step, max_number):
        self.problem = problem
        self.step = step
        self.max_number = max_number

    def run1(self):
        array = [0]
        prev_idx = 0
        for i in range(1, self.max_number + 1):
            idx = (prev_idx + self.step) % len(array) + 1
            array.insert(idx, i)
            prev_idx = idx

        idx = array.index(self.max_number)
        return array[(idx + 1) % len(array)]

    def run(self):
        if self.problem == 1:
            return self.run1()

        zero_idx = 0
        after_zero = 0

        prev_idx = 0
        for i in range(1, self.max_number + 1):
            idx = (prev_idx + self.step) % i

            if idx == zero_idx:
                after_zero = i
            if idx < zero_idx:
                zero_idx += 1

            prev_idx = idx + 1

        return after_zero

def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

run(3, 2017) | eq(638)

run(371, 2017) | debug('Star 1') | eq(1311)

run2(3, 4) | eq(2)
run2(3, 8) | eq(5)
run2(3, 9) | eq(9)
run2(371, 50000000) | debug('Star 2') | eq(39170601)
