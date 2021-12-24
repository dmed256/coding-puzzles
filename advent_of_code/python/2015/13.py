import itertools
from repo_utils import *

def parse_values(lines):
    values = {}
    names = set()
    for line in lines:
        words = line[:-1].split(' ')
        c1 = words[0]
        c2 = words[-1]
        value = [
            int(word)
            for word in words
            if word.isdigit()
        ][0]
        if 'lose' in words:
            value = -value

        values[(c1, c2)] = value
        names.add(c1)
        names.add(c2)
    return (values, names)

def get_happiness(values, order):
    prev_name = order[-1]
    happiness = 0
    for name in order:
        happiness += values[(name, prev_name)]
        happiness += values[(prev_name, name)]
        prev_name = name
    return happiness

def run(lines, problem = 1):
    (values, names) = parse_values(lines)
    if problem == 2:
        for name in names:
            values[(name, 'You')] = 0
            values[('You', name)] = 0
        names = (*names, 'You')
    return max((
        get_happiness(values, order)
        for order in itertools.permutations(names)
    ))

example1 = multiline_lines("""
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
""")

run(example1) | eq(330)

input_lines = get_input_lines()

run(input_lines) | debug('Star 1')

run(input_lines, 2) | debug('Star 2')
