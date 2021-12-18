from repo_utils import *

def run(problem, input_value):
    if problem == 1:
        recipes = int(input_value)
    else:
        recipes = 1e40

    values = [3, 7]
    ptr1 = 0
    ptr2 = 1
    while len(values) < recipes + 10:
        v1 = values[ptr1]
        v2 = values[ptr2]

        # Max of 9 + 9 = 18 (2 digits)
        values += [
            int(d)
            for d in str(v1 + v2)
        ]

        ptr1 = (ptr1 + 1 + v1) % len(values)
        ptr2 = (ptr2 + 1 + v2) % len(values)

        if problem == 1:
            continue

        scoreboard = ''.join([
            str(d)
            for d in values[-len(input_value) - 2:]
        ])
        if input_value not in scoreboard:
            continue

        input_index = scoreboard.index(input_value)
        return len(values) - len(scoreboard) + input_index

    return ''.join(
        str(d)
        for d in values[recipes:recipes + 10]
    )

run(1, '9') | eq('5158916779')
run(1, '5') | eq('0124515891')
run(1, '18') | eq('9251071085')
run(1, '2018') | eq('5941429882')

run(1, '030121') | debug('Star 1') | eq('5101271252')

run(2, '51589') | eq(9)
run(2, '01245') | eq(5)
run(2, '92510') | eq(18)
run(2, '59414') | eq(2018)

run(2, '030121') | debug('Star 2') | eq(20287556)
