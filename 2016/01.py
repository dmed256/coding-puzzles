from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

def run(problem, lines):
    values = lines[0].split(', ')

    pos = (0, 0)
    direction = UP
    for value in values:
        turn = value[0]
        dist = int(value[1:])
        if turn == 'R':
            direction = CLOCKWISE[direction]
        else:
            direction = COUNTER_CLOCKWISE[direction]
        pos = (pos[0] + dist * direction[0], pos[1] + dist * direction[1])
    return(abs(pos[0]) + abs(pos[1]))

run(1, input_lines) | debug('Star 1') | eq(241)

# run(2, example1) | eq()

# run(2, input_lines) | debug('Star 2') | clipboard()
