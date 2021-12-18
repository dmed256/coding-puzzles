from repo_utils import *

input_lines = get_input_lines()

class Character(BaseModel):
    y: int
    x: int
    type: str
    id: int = 0
    attack: int = 3
    health: int= 200

enemy_type_map = {
    'G': 'E',
    'E': 'G',
}

READING_DIRECTIONS = [
    GRID_UP,
    GRID_LEFT,
    GRID_RIGHT,
    GRID_DOWN,
]

def find_target(grid, char, characters):
    enemy_type = enemy_type_map[char.type]

    queue = [(0, char.y, char.x)]
    paths = {
        (char.x, char.y): [],
    }
    # TODO: Check here
    while queue:
        steps, y, x = heapq.heappop(queue)
        pos = (x, y)

        for npos in grid.neighbors(pos, READING_DIRECTIONS):
            if npos in paths:
                continue

            nx, ny = npos
            v = grid[npos]

            if v == '#':
                continue

            path = paths[pos] + [npos]

            if v == '.':
                heapq.heappush(queue, (steps + 1, ny, nx))
                paths[npos] = path

            if v == enemy_type:
                return path

    return None


def find_enemy(grid, char, char_positions):
    pos = (char.x, char.y)

    direct_enemies = sorted([
        other
        for npos in grid.neighbors(pos)
        if (other := char_positions.get(npos))
        and other.type != char.type
    ], key=lambda other: (other.health, other.y, other.x))

    return direct_enemies and direct_enemies[0]


def run(problem, lines):
    grid = Grid(lines)

    def print_state():
        grid.print()
        for char in characters:
            print(1, char)

    characters = [
        Character(
            y=y,
            x=x,
            type=c,
        )
        for (x, y), c in grid
        if c in 'GE'
    ]
    for i, char in enumerate(characters):
        char.id = i

    character_positions = {
        (char.x, char.y): char
        for char in characters
    }

    for full_rounds in range(100000000):
        characters = sorted([
            char
            for char in characters
            if 0 < char.health
        ], key=lambda char: (char.y, char.x))

        for active_char in list(characters):
            if active_char.health <= 0:
                continue

            has_enemies = any(
                char
                for char in characters
                if char.type != active_char.type
            )

            # We finished the game!
            if not has_enemies:
                total_health = sum(
                    max(0, char.health)
                    for char in characters
                )
                return total_health * full_rounds

            # First find the target we're aiming for
            other_characters = [
                char
                for char in characters
                if char.id != active_char.id
            ]
            path = find_target(
                grid,
                active_char,
                other_characters,
            )

            # No way to move or attack
            if path is None:
                continue

            # Move towards a unit
            if path[0] not in character_positions:
                pos = path.pop(0)
                char_pos = (active_char.x, active_char.y)

                grid[char_pos] = '.'
                grid[pos] = active_char.type

                active_char.x = pos[0]
                active_char.y = pos[1]

                character_positions = {
                    (char.x, char.y): char
                    for char in characters
                }

            # Check if there's an enemy to attack
            target = find_enemy(grid, active_char, character_positions)
            if not target:
                continue

            # Attack!
            target.health -= active_char.attack
            if 0 < target.health:
                continue

            # Kill 'em!!!!
            grid[(target.x, target.y)] = '.'
            characters = [
                char
                for char in characters
                if 0 < char.health
            ]
            character_positions = {
                (char.x, char.y): char
                for char in characters
            }


# example = multiline_lines(r"""
# #######
# #.G...#
# #...EG#
# #.#.#G#
# #..G#E#
# #.....#
# #######
# """)
# run(1, example) | eq(27730)

# example = multiline_lines(r"""
# #######
# #G..#E#
# #E#E.E#
# #G.##.#
# #...#E#
# #...E.#
# #######
# """)
# run(1, example) | eq(36334)

# example = multiline_lines(r"""
# #######
# #E..EG#
# #.#G.E#
# #E.##E#
# #G..#.#
# #..E#.#
# #######
# """)
# run(1, example) | eq(39514)

# example = multiline_lines(r"""
# #######
# #E.G#.#
# #.#G..#
# #G.#.G#
# #G..#.#
# #...E.#
# #######
# """)
# run(1, example) | eq(27755)

# example = multiline_lines(r"""
# #######
# #.E...#
# #.#..G#
# #.###.#
# #E#G#G#
# #...#G#
# #######
# """)
# run(1, example) | eq(28944)

# example = multiline_lines(r"""
# #########
# #G......#
# #.E.#...#
# #..##..G#
# #...##..#
# #...#...#
# #.G...G.#
# #.....G.#
# #########
# """)
# run(1, example) | eq(18740)

# low: 23820
# high: 198855
# high: 198855
run(1, input_lines) | submit(1)
