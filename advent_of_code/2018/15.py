from repo_utils import *

input_lines = get_input_lines()

Character = namedtuple(
    'Character',
    ['y', 'x', 'type', 'attack', 'health'],
)

def find_target(grid, char, characters):


def run(problem, lines):
    grid = Grid(lines)

    characters = [
        Character(y, x, c, 3, 200)
        for (x, y), c in grid
        if c in 'GE'
    ]
    heapq.heapify(characters)

    for full_rounds in range(100000000):
        next_characters = []
        while characters:
            char = heapq.heappop(characters)

            # First find the target we're aiming for
            char_target = find_target(grid, char, characters)
            next_char_target = find_target(grid, char, next_characters)
            target = char_target or next_char_target

            # We finished the game!
            if target is None:
                total_health = sum(
                    char.health
                    for char in characters + next_characters
                )
                return total_health * full_rounds

            if char_target is not None:
                target = char_target
                target_in_characters = True
            else:
                target = next_char_target
                target_in_characters = False

            dist = abs(char.x - target.x) + abs(char.y - target.y)
            if dist == 1:
                target.health -= char.attack
                if target.health <= 0:
                    pass

            # Check if we need to walk
            walk_to_target(grid, char, target)
            heapq.heappush(next_characters, char)

        characters = next_characters

example = multiline_lines(r"""
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
""")
run(1, example) | eq(27730)

example = multiline_lines(r"""
#######       #######
#G..#E#       #...#E#   E(200)
#E#E.E#       #E#...#   E(197)
#G.##.#  -->  #.E##.#   E(185)
#...#E#       #E..#E#   E(200), E(200)
#...E.#       #.....#
#######       #######
""")
run(1, example) | eq(36334)

example = multiline_lines(r"""
#######       #######
#E..EG#       #.E.E.#   E(164), E(197)
#.#G.E#       #.#E..#   E(200)
#E.##E#  -->  #E.##.#   E(98)
#G..#.#       #.E.#.#   E(200)
#..E#.#       #...#.#
#######       #######
""")
run(1, example) | eq(39514)

example = multiline_lines(r"""
#######       #######
#E.G#.#       #G.G#.#   G(200), G(98)
#.#G..#       #.#G..#   G(200)
#G.#.G#  -->  #..#..#
#G..#.#       #...#G#   G(95)
#...E.#       #...G.#   G(200)
#######       #######
""")
run(1, example) | eq(27755)

example = multiline_lines(r"""
#######       #######
#.E...#       #.....#
#.#..G#       #.#G..#   G(200)
#.###.#  -->  #.###.#
#E#G#G#       #.#.#.#
#...#G#       #G.G#G#   G(98), G(38), G(200)
#######       #######
""")
run(1, example) | eq(28944)

example = multiline_lines(r"""
#########       #########
#G......#       #.G.....#   G(137)
#.E.#...#       #G.G#...#   G(200), G(200)
#..##..G#       #.G##...#   G(200)
#...##..#  -->  #...##..#
#...#...#       #.G.#...#   G(200)
#.G...G.#       #.......#
#.....G.#       #.......#
#########       #########
""")
run(1, example) | eq(18740)

run(1, input_lines) | submit(1)
