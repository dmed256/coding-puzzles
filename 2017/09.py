from advent_of_code import *

input_value = get_input()

class Problem:
    def __init__(self, problem, line):
        self.problem = problem
        self.line = line

    def run(self):
        line = self.line

        clean_line = ''
        garbage_chars = 0

        in_garbage = False
        escaping = False
        for c in line:
            if not in_garbage:
                in_garbage = c == '<'
                if in_garbage:
                    continue

            if not in_garbage:
                clean_line += c
                continue

            if escaping:
                escaping = False
            elif c == '>':
                in_garbage = False
            else:
                escaping = (c == '!')
                garbage_chars += not escaping

        if self.problem == 2:
            return garbage_chars

        depth = 0
        score = 0
        for c in clean_line:
            if c == '{':
                depth += 1
            elif c == '}':
                score += depth
                depth -= 1

        return score

def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

run('<>') | eq(0)
run('<random characters>') | eq(0)
run('<<<<>') | eq(0)
run('<{!>}>') | eq(0)
run('<!!>') | eq(0)
run('<!!!>>') | eq(0)
run('<{o"i!a,<{i<a>') | eq(0)

run('{}') | eq(1)
run('{{{}}}') | eq(6)
run('{{},{}}') | eq(5)
run('{{{},{},{{}}}}') | eq(16)
run('{<a>,<a>,<a>,<a>}') | eq(1)
run('{{<ab>},{<ab>},{<ab>},{<ab>}}') | eq(9)
run('{{<!!>},{<!!>},{<!!>},{<!!>}}') | eq(9)
run('{{<a!>},{<a!>},{<a!>},{<ab>}}') | eq(3)

run(input_value) | debug('Star 1') | eq(10800)

run2('<>') | eq(0)
run2('<random characters>') | eq(17)
run2('<<<<>') | eq(3)
run2('<{!>}>') | eq(2)
run2('<!!>') | eq(0)
run2('<!!!>>') | eq(0)
run2('<{o"i!a,<{i<a>') | eq(10)

run2(input_value) | debug('Star 2') | eq(4522)
