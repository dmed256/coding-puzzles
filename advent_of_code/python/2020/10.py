from repo_utils import *

input_value = get_input()
input_lines = get_input_lines()

def get_diffs(lines):
    values = sorted([int(v) for v in lines])
    values = [0] + values + [3 + values[-1]]

    charges = []
    for i in range(1, len(values)):
        charges.append(values[i] - values[i - 1])
    return charges

def run(lines):
    diffs = get_diffs(lines)

    ones = len([d for d in diffs if d == 1])
    threes = len([d for d in diffs if d == 3])

    return ones * threes


example1 = multiline_lines(r"""
16
10
15
5
1
11
7
19
6
12
4
""")

example2 = multiline_lines(r"""
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
""")

run(example1) | eq(35)
run(example2) | eq(220)
run(input_lines) | debug('Star 1') | eq(2244)

def run2(lines):
    diffs = get_diffs(lines)

    groups = [1]
    for d in diffs:
        if d == 1:
            groups[-1] += 1
        else:
            groups.append(1)

    groups = [
        group
        for group in groups
        if group
    ]
    combinations = {
        1: 1,
        2: 1,
        3: 2,
        4: 4,
        5: 7
    }
    value = 1
    for group in groups:
        value *= combinations[group]
    return value

run2(example1) | eq(8)
run2(example2) | eq(19208)
run2(input_lines) | debug('Star 2') | eq(3947645370368)
