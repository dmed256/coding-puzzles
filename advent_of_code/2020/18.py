import re
from repo_utils import *

input_value = get_input()
input_lines = get_input_lines()

def apply_operator(parts, valid_op=None):
    next_parts = [parts[0]]
    for i in range(1, len(parts), 2):
        left = int(next_parts[-1])
        op = parts[i]
        right = int(parts[i + 1])

        if valid_op and op != valid_op:
            next_parts.append(op)
            next_parts.append(right)
            continue

        if op == '+':
            next_parts[-1] = left + right
        elif op == '*':
            next_parts[-1] = left * right

    return next_parts

def direct_compute(s, problem):
    parts = re.split('([*+])', s)

    if problem == 1:
        parts = apply_operator(parts)
    else:
        for valid_op in ['+', '*']:
            parts = apply_operator(parts, valid_op)

    return parts[0]

def compute(line, problem):
    line = line.replace(' ', '')

    stack = ['']
    for c in line:
        if c == '(':
            stack.append('')
        elif c == ')':
            value = direct_compute(stack.pop(), problem)
            stack[-1] += str(value)
        else:
            stack[-1] += c

    return direct_compute(stack[-1], problem)

def run(lines, problem):
    return sum([
        compute(line, problem)
        for line in lines
    ])

example1 = multiline_lines(r"""
1 + 2 * 3 + 4 * 5 + 6
""")

example2 = multiline_lines(r"""
1 + (2 * 3) + (4 * (5 + 6))
""")

example3 = multiline_lines(r"""
2 * 3 + (4 * 5)
""")

example4 = multiline_lines(r"""
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2
""")

run(example1, 1) | eq(71)
run(example2, 1) | eq(51)
run(example3, 1) | eq(26)
run(example4, 1) | eq(13632)
run(input_lines, 1) | debug('Star 1') | eq(86311597203806)

run(example1, 2) | eq(231)
run(example2, 2) | eq(51)
run(example3, 2) | eq(46)
run(example4, 2) | eq(23340)
run(input_lines, 2) | debug('Star 2') | eq(276894767062189)
