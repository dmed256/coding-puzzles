from advent_of_code import *

def run(s, find_depth=None):
    depth = 0
    for i, char in enumerate(s):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        if depth == find_depth:
            return i + 1

    return depth

run('(())') | eq(0)
run('()()') | eq(0)
run('(((') | eq(3)
run('(()(()(') | eq(3)
run('))(((((') | eq(3)
run('())') | eq(-1)
run('))(') | eq(-1)
run(')))') | eq(-3)
run(')())())') | eq(-3)

test_input = get_input()

run(test_input) | debug('Star 1')

run(')', -1) | eq(1)
run('()())', -1) | eq(5)

run(test_input, -1) | debug('Star 2')
