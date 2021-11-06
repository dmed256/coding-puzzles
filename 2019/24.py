from advent_of_code import *
from int_processor import *

# . . . . .
# . x . . .
# . . . . .



def parse_lines(lines):
    grid = Grid([
        [int(v == '#') for v in line]
        for line in lines
    ])
    return sum([
        2**(x + 5*y)
        for (x, y, v) in grid
        if v
    ])

def print_score(score):
    output = ''
    for y in range(5):
        for x in range(5):
            idx = 2**(x + 5*y)
            output += '#' if score & idx else '.'
        output += '\n'
    print(output)

def apply_timestep(score):
    next_score = 0
    for y in range(5):
        for x in range(5):
            idx_score = 2**(x + 5*y)
            v = score & idx_score
            neighbors = sum([
                bool(score & 2**(x + dx + 5*(y + dy)))
                for dx, dy in DIRECTIONS
                if 0 <= (x + dx) < 5
                and 0 <= (y + dy) < 5
            ])
            if (v and neighbors == 1) or (not v and 1 <= neighbors <= 2):
                next_score += idx_score

    return next_score

example1 = multiline_lines("""
....#
#..#.
#..##
..#..
#....
""")

score = parse_lines(example1)
for i in range(5):
    print_score(score)
    score = apply_timestep(score)

example2 = multiline_lines("""
.....
.....
.....
#....
.#...
""")

parse_lines(example2) | eq(2129920)

input_lines = get_input_lines()
score = parse_lines(input_lines)

scores = set()
while score not in scores:
    scores.add(score)
    score = apply_timestep(score)

score | debug('Star 1')
