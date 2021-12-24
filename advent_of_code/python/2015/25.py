from repo_utils import *

class Problem:
    def __init__(self, problem, row, column):
        self.problem = problem
        self.row = row - 1
        self.column = column - 1

    def run(self):
        row = self.row
        col = self.column

        distance = row + col
        if distance > 0:
            # 1 + 2 + 3 + ... distance
            offset = distance * (1 + distance) // 2
        else:
            offset = 0

        # Add diag offset
        offset += col

        value = 20151125
        for i in range(offset):
            value = (value * 252533) % 33554393
        return value

def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

run(1, 1) | eq(20151125)
run(2, 1) | eq(31916031)
run(1, 2) | eq(18749137)
run(6, 3) | eq(25397450)
run(6, 6) | eq(27995004)
run(2978, 3083) | debug('Star 1') | eq(2650453)
