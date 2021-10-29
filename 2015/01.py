from advent_of_code import *

@testable
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

run('(())').should_be(0)
run('()()').should_be(0)
run('(((').should_be(3)
run('(()(()(').should_be(3)
run('))(((((').should_be(3)
run('())').should_be(-1)
run('))(').should_be(-1)
run(')))').should_be(-3)
run(')())())').should_be(-3)

test_input = get_input()

run(test_input).debug('Star 1')

run(')', -1).should_be(1)
run('()())', -1).should_be(5)

run(test_input, -1).debug('Star 2')
