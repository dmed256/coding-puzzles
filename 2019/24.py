from advent_of_code import *
from int_processor import *

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
            bit_value = 2**(x + 5*y)
            bit_set = score & bit_value
            neighbors = sum([
                bool(score & 2**(x + dx + 5*(y + dy)))
                for dx, dy in DIRECTIONS
                if 0 <= (x + dx) < 5
                and 0 <= (y + dy) < 5
            ])
            if ((bit_set and neighbors == 1) or
                (not bit_set and 1 <= neighbors <= 2)):
                next_score += bit_value

    return next_score

example1 = multiline_lines("""
.....
.....
.....
#....
.#...
""")

parse_lines(example1) | eq(2129920)

input_lines = get_input_lines()
score = parse_lines(input_lines)

scores = set()
while score not in scores:
    scores.add(score)
    score = apply_timestep(score)

score | debug('Star 1') | eq(2130474)

def get_mid_bugs(score, direction):
    if direction == RIGHT:
        return sum(
            bool(score & (1 << 5*y))
            for y in range(5)
        )
    if direction == LEFT:
        return sum(
            bool(score & (1 << (4 + 5*y)))
            for y in range(5)
        )
    if direction == DOWN:
        return sum(
            bool(score & (1 << x))
            for x in range(5)
        )
    if direction == UP:
        return sum(
            bool(score & (1 << (20 + x)))
            for x in range(5)
        )

def apply_timestep2(outer_score, score, inner_score):
    next_score = 0
    for y in range(5):
        for x in range(5):
            if (x, y) == (2, 2):
                continue

            bit_value = 2**(x + 5*y)
            bit_set = score & bit_value
            neighbors = [
                (x + dx, y + dy)
                for dx, dy in DIRECTIONS
                if 0 <= (x + dx) < 5
                and 0 <= (y + dy) < 5
            ]
            neighbor_count = sum([
                bool(score & 2**(x2 + 5*y2))
                for (x2, y2) in neighbors
                if (x2, y2) != (2, 2)
            ])
            mid_direction = [
                direction
                for direction in DIRECTIONS
                if (2, 2) == apply_direction((x, y), direction)
            ]
            if mid_direction:
                neighbor_count += get_mid_bugs(inner_score, mid_direction[0])

            # Apply the outer bugs
            if y == 0:
                neighbor_count += bool(outer_score & (1 << 7))
            if y == 4:
                neighbor_count += bool(outer_score & (1 << 17))
            if x == 0:
                neighbor_count += bool(outer_score & (1 << 11))
            if x == 4:
                neighbor_count += bool(outer_score & (1 << 13))

            if ((bit_set and neighbor_count == 1) or
                (not bit_set and 1 <= neighbor_count <= 2)):
                next_score += bit_value

    return next_score

def apply_timesteps(score, timestep_count):
    scores = {0: score}

    for timestep in range(timestep_count):
        min_depth = min(scores.keys()) - 1
        max_depth = max(scores.keys()) + 1
        new_scores = {}
        for depth in range(min_depth, max_depth + 1):
            depth_score = apply_timestep2(
                scores.get(depth - 1, 0),
                scores.get(depth, 0),
                scores.get(depth + 1, 0),
            )
            if depth_score:
                new_scores[depth] = depth_score
        scores = new_scores

    return scores

def get_scores_bugs(scores):
    return sum(
        bool(score & (1 << bit))
        for score in scores.values()
        for bit in range(25)
    )

example1 = multiline_lines("""
....#
#..#.
#..##
..#..
#....
""")
score = parse_lines(example1)
get_scores_bugs(
    apply_timesteps(score, 10)
) | eq(99)

input_lines = get_input_lines()
score = parse_lines(input_lines)

get_scores_bugs(
    apply_timesteps(score, 200)
) | debug('Star 2') | eq(1923)
