from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

def parse_lines(lines):
    word = lines[-1]
    lines = lines[:-2]

    replacements = []
    for line in lines:
        [a, b] = line.split(' => ')
        replacements.append((a, b))

    return word, replacements

def find_replacements(word, c1, c2):
    replacements = set()
    for i in range(len(word)):
        if word[i:i+len(c1)] != c1:
            continue
        replacement = word[:i] + c2 + word[i+len(c1):]
        if replacement not in replacements:
            yield replacement
        replacements.add(replacement)

def find_combinations(word, replacements):
    combinations = set()
    for (c, c2) in replacements:
        combinations.update(
            find_replacements(word, c, c2)
        )
    return combinations

def run(lines):
    word, replacements = parse_lines(lines)
    return len(find_combinations(word, replacements))

example1 = multiline_lines(r"""
H => HO
H => OH
O => HH

HOH
""")

run(example1) | eq(4)
run(input_lines) | debug('Star 1')

def run2(lines):
    end_value, replacements = parse_lines(lines)

    inv_replacements = {
        c2: c1
        for c1, c2 in replacements
    }

    return changes

example1 = multiline_lines(r"""
e => H
e => O
H => HO
H => OH
O => HH

HOH
""")

example2 = multiline_lines(r"""
e => H
e => O
H => HO
H => OH
O => HH

HOHOHO
""")

run2(example1) | eq(3)
run2(example2) | eq(6)

# Too low: 195
# Too high: 8071006
run2(input_lines) | debug('Star 2')
