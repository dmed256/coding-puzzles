from advent_of_code import *

@testable
def run(s):
    houses = {(0, 0): True}
    x = 0
    y = 0
    for c in s.strip():
        if c == '<':
            x -= 1
        elif c == '>':
            x += 1
        elif c == '^':
            y += 1
        elif c == 'v':
            y -= 1
        houses[(x, y)] = True
    return len(houses.keys())

run('>').should_be(2)
run('^>v<').should_be(4)
run('^v^v^v^v^v').should_be(2)

test_input = get_input()

run(test_input).debug('Star 1')

@testable
def run2(s):
    houses = {(0, 0): True}
    x = [0, 0]
    y = [0, 0]
    santa = 0
    for c in s.strip():
        if c == '<':
            x[santa] -= 1
        elif c == '>':
            x[santa] += 1
        elif c == '^':
            y[santa] += 1
        elif c == 'v':
            y[santa] -= 1

        houses[(x[santa], y[santa])] = True
        santa = (santa + 1) % 2

    return len(houses.keys())

run2('^v').should_be(3)
run2('^>v<').should_be(3)
run2('^v^v^v^v^v').should_be(11)

test_input = get_input()

run2(test_input).debug('Star 2')
