from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

def run(problem, lines):
    values = [
        [int(x.strip()) for x in line.split()]
        for line in lines
    ]

    if problem == 2:
        vert_values = []
        for c in range(3):
            for r in range(0, len(values), 3):
                vert_values.append((
                    values[r][c],
                    values[r + 1][c],
                    values[r + 2][c],
                ))
        values = vert_values

    return len([
        1
        for a, b, c in values
        if (a + b > c and
            a + c > b and
            b + c > a)
    ])

run(1, input_lines) | debug('Star 1') | eq(1050)

run(2, input_lines) | debug('Star 2') | eq(1921)
