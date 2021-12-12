from repo_utils import *

input_lines = get_input_lines()

def is_valid_password(line):
    [counts, letter, password] = line.split(' ')
    letter = letter[0]
    [min_count, max_count] = [int(c) for c in counts.split('-')]

    letter_count = len([c for c in password if c == letter])
    return min_count <= letter_count <= max_count

def run(lines):
    return len([
        line
        for line in lines
        if is_valid_password(line)
    ])

example = multiline_lines(r"""
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
""")

run(example) | eq(2)

run(input_lines) | debug('Star 1') | eq(645)

def is_valid_password2(line):
    [counts, letter, password] = line.split(' ')
    letter = letter[0]
    [i1, i2] = [int(c) - 1 for c in counts.split('-')]

    return 1 == (password[i1] == letter) + (password[i2] == letter)

def run2(lines):
    return len([
        line
        for line in lines
        if is_valid_password2(line)
    ])

run2(example) | eq(1)

run2(input_lines) | debug('Star 2') | eq(737)
