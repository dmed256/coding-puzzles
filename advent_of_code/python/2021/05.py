from repo_utils import *

input_value = get_input()
input_lines = get_input_lines()

class Problem:
    def __init__(self, problem, lines):
        self.problem = problem

        self.hlines = []
        self.vlines = []
        self.dlines = []
        for line in lines:
            [left, right] = line.split(' -> ')
            [x1_, y1_] = [int(x) for x in left.split(',')]
            [x2_, y2_] = [int(x) for x in right.split(',')]

            x1, x2 = min(x1_, x2_), max(x1_, x2_)
            y1, y2 = min(y1_, y2_), max(y1_, y2_)

            if x1 == x2:
                self.vlines.append([x1, [y1, y2]])
            elif y1 == y2:
                self.hlines.append([y1, [x1, x2]])
            else:
                self.dlines.append([[x1_, y1_], [x2_, y2_]])

    def run(self):
        counts = {}
        for [x, [y1, y2]] in self.vlines:
            for y in range(y1, y2 + 1):
                k = (x, y)
                if k in counts:
                    counts[k] += 1
                else:
                    counts[k] = 1

        for [y, [x1, x2]] in self.hlines:
            for x in range(x1, x2 + 1):
                k = (x, y)
                if k in counts:
                    counts[k] += 1
                else:
                    counts[k] = 1

        if self.problem == 2:
            for [[x1, y1], [x2, y2]] in self.dlines:
                length = max(x1, x2) - min(x1, x2) + 1
                dx = 1 if x1 <= x2 else -1
                dy = 1 if y1 <= y2 else -1
                for i in range(length):
                    k = (x1 + dx*i, y1 + dy*i)
                    if k in counts:
                        counts[k] += 1
                    else:
                        counts[k] = 1

        return len([
            1
            for count in counts.values()
            if count > 1
        ])

def run(lines):
    return Problem(1, lines).run()

def run2(lines):
    return Problem(2, lines).run()

example1 = multiline_lines(r"""
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
""")

run(example1) | eq(5)

run(input_lines) | debug('Star 1') | eq(4993)

run2(example1) | eq(12)

run2(input_lines) | debug('Star 2') | eq(21101)
