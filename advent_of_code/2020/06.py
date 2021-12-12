from repo_utils import *

input_lines = get_input_lines()

def split_groups(lines):
    groups = [[]]
    for line in lines:
        if line:
            groups[-1].append(line)
        else:
            groups[-1] = ' '.join(groups[-1])
            groups.append([])
    groups[-1] = ' '.join(groups[-1])
    return groups

def run(lines):
    return sum([
        len(set(sorted(group.replace(' ', ''))))
        for group in split_groups(lines)
    ])

example1 = multiline_lines(r"""
abcx
abcy
abcz
""")

example2 = multiline_lines(r"""
abc

a
b
c

ab
ac

a
a
a
a

b
""")

run(example1) | eq(6)
run(example2) | eq(11)

run(input_lines) | debug('Star 1') | eq(6878)

def run2(lines):
    value = 0
    for group in split_groups(lines):
        counts = {}
        people_answers = group.split(' ')
        for person in people_answers:
            for c in set(person):
                counts[c] = counts.get(c, 0) + 1
        value += len([
            k
            for k, v in counts.items()
            if v == len(people_answers)
        ])
    return value

run2(example2) | eq(6)
run2(input_lines) | debug('Star 2') | eq(3464)
