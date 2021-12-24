from repo_utils import *

input_lines = get_input_lines()

def apply_reactions(value):
    value = [c for c in value]

    ptr = 0
    while ptr < len(value) - 1:
        c1, c2 = value[ptr:ptr + 2]
        if c1 == c2 or c1.lower() != c2.lower():
            ptr += 1
            continue

        del value[ptr:ptr + 2]
        ptr = max(0, ptr - 1)

    return value

def run(problem, lines):
    value = lines[0]

    if problem == 1:
        return len(apply_reactions(value))

    chars = {c.lower() for c in value}
    return min(
        len(apply_reactions(
            value.replace(c, '').replace(c.upper(), '')
        ))
        for c in chars
    )

run(1, ['dabAcCaCBAcCcaDA']) | eq(10)

run(1, input_lines) | debug('Star 1') | eq(11636)

run(2, ['dabAcCaCBAcCcaDA']) | eq(4)

run(2, input_lines) | debug('Star 2') | eq(5302)
