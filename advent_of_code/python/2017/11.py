from repo_utils import *

def run(line):
    pos = (0, 0)
    hex_directions = {
        'n': (0, 2),
        'ne': (1, 1),
        'se': (1, -1),
        's': (0, -2),
        'sw': (-1, -1),
        'nw': (-1, 1),
    }
    max_dist = 0
    for v in line.split(','):
        pos = apply_direction(pos, hex_directions[v])
        (x, y) = pos
        dist = (abs(x) + abs(y)) // 2
        max_dist = max(dist, max_dist)

    return [dist, max_dist]

run('ne,ne,ne')[0] | eq(3)
run('ne,ne,sw,sw')[0] | eq(0)
run('ne,ne,s,s')[0] | eq(2)
run('se,sw,se,sw,sw')[0] | eq(3)

input_value = get_input()

run(input_value)[0] | debug('Star 1') | eq(747)

run(input_value)[1] | debug('Star 2') | eq(1544)
