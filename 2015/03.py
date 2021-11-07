from advent_of_code import *

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

run('>') | eq(2)
run('^>v<') | eq(4)
run('^v^v^v^v^v') | eq(2)

test_input = get_input()

run(test_input) | debug('Star 1')

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

run2('^v') | eq(3)
run2('^>v<') | eq(3)
run2('^v^v^v^v^v') | eq(11)

test_input = get_input()

run2(test_input) | debug('Star 2')
