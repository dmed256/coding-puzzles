from repo_utils import *

input_lines = get_input_lines()

class Character(BaseModel):
    pos: Any
    type: str
    id: int = 0
    attack: int = 3
    health: int = 200

enemy_type_map = {
    'G': 'E',
    'E': 'G',
}


def move_to_target(grid, active_char, enemies):
    x, y = active_char.pos

    queue = [(0, y, x, [])]
    visited = set()
    attacking_spots = []
    while queue:
        steps, y, x, path = heapq.heappop(queue)
        pos = (x, y)

        if pos in visited:
            continue
        visited.add(pos)

        if attacking_spots and attacking_spots[0][0] < steps:
            break

        # Check if there are enemies around
        neighbors = [
            npos
            for npos in grid.neighbors(pos)
        ]
        if any(npos in enemies for npos in neighbors):
            heapq.heappush(
                attacking_spots,
                (steps, pos[1], pos[0], path),
            )
            continue

        for npos in neighbors:
            v = grid[npos]
            if v in ['#', active_char.type]:
                continue

            heapq.heappush(
                queue,
                (steps + 1, npos[1], npos[0], path + [npos]),
            )

    # Nothing to do
    if not attacking_spots:
        return

    print(active_char)
    print(attacking_spots)
    min_steps = attacking_spots[0][0]
    next_stops = {
        path[0]
        for steps, _, _, path in attacking_spots
        if steps == min_steps
    }

    _, _, next_pos = sorted([
        (pos[1], pos[0], pos)
        for pos in next_stops
    ])[0]

    grid[active_char.pos] = '.'
    active_char.pos = next_pos
    grid[active_char.pos] = active_char.type

def parse_lines(lines):
    grid = Grid(lines)

    characters = [
        Character(
            pos=pos,
            type=c,
        )
        for pos, c in grid
        if c in 'GE'
    ]
    for i, char in enumerate(characters):
        char.id = i

    return grid, characters


def play_round(grid, characters):
    def turn_order_key(char):
        return (char.pos[1], char.pos[0])

    def find_adjacent_target(char, enemies):
        return min(
            [
                enemies[npos]
                for npos in grid.neighbors(char.pos)
                if npos in enemies
            ],
            key=lambda char: char.health,
            default=None,
        )

    def attack_target(active_char, target):
        target.health -= active_char.attack
        target.health = max(0, target.health)

        if 0 < target.health:
            return

        grid[target.pos] = '.'
        target_idx = [
            idx
            for idx, char in enumerate(characters)
            if char.id == target.id
        ][0]
        characters.pop(target_idx)

    for active_char in sorted(characters, key=turn_order_key):
        if active_char.health <= 0:
            continue

        enemies = {
            char.pos: char
            for char in characters
            if char.type != active_char.type
        }
        if not enemies:
            return True

        target = find_adjacent_target(active_char, enemies)
        if target is not None:
            attack_target(active_char, target)
            continue

        move_to_target(grid, active_char, enemies)

        target = find_adjacent_target(active_char, enemies)
        if target is not None:
            attack_target(active_char, target)

    return False


def run(problem, lines):
    raise 1
    grid, characters = parse_lines(lines)
    full_rounds = 0

    def print_state():
        grid.print()
        for char in characters:
            print(char)

        print(f'Round: {full_rounds}')
        input()

    for full_rounds in range(100000000):
        finished = play_round(grid, characters)
        if finished:
            break

        print_state()

    total_health = sum(
        char.health
        for char in characters
    )
    return full_rounds * total_health


example = multiline_lines(r"""
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
""")
# run(1, example) | eq(27730)

example = multiline_lines(r"""
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######
""")
run(1, example) | eq(36334)
raise 1

example = multiline_lines(r"""
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
""")
run(1, example) | eq(39514)

example = multiline_lines(r"""
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######
""")
run(1, example) | eq(27755)

example = multiline_lines(r"""
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######
""")
run(1, example) | eq(28944)

example = multiline_lines(r"""
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########
""")
run(1, example) | eq(18740)

# low:  23820
# high: 198855
# high: 198855
# ???:  195372
run(1, input_lines) | submit(1)
