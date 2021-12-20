from repo_utils import *

input_lines = get_input_lines()

DEBUG = False
DEBUG_CHARACTERS = False
DEBUG_ROUNDS = False
MANUAL_SKIP = False

class Character(BaseModel):
    pos: Any
    type: str
    id: int = 0
    attack: int = 3
    health: int = 200

    @property
    def is_dead(self):
        return self.health <= 0

enemy_type_map = {
    'G': 'E',
    'E': 'G',
}

def print_skip(grid, characters, active_char):
    if not DEBUG:
        return

    grid = grid.copy()
    grid[active_char.pos] = yellow('?')

    grid.print()

    if DEBUG_CHARACTERS:
        print('Char:')
        print(active_char)

        print('\nOthers:')
        for char in characters:
            if char.id != active_char.id:
                print(char)

    print('\n')
    if MANUAL_SKIP:
        input()

def print_move(grid, characters, active_char, next_pos):
    if not DEBUG:
        return

    grid = grid.copy()
    grid[active_char.pos] = yellow(grid[active_char.pos])
    grid[next_pos] = red('@')

    grid.print()

    if DEBUG_CHARACTERS:
        print('Char:')
        print(active_char)

        print('\nOthers:')
        for char in characters:
            if char.id != active_char.id:
                print(char)

    print('\n')
    if MANUAL_SKIP:
        input()


def print_attack(grid, characters, active_char, target):
    if not DEBUG:
        return

    grid = grid.copy()
    grid[active_char.pos] = yellow(grid[active_char.pos])
    grid[target.pos] = red(grid[target.pos])

    grid.print()

    if DEBUG_CHARACTERS:
        print('Char:')
        print(active_char)

        print('Target:')
        print(target)

        print('\nOthers:')
        for char in characters:
            if char.id not in [active_char.id, target.id]:
                print(char)

    print('\n')
    if MANUAL_SKIP:
        input()


def find_attacking_spot(grid, active_char, characters):
    enemy_type = enemy_type_map[active_char.type]

    x, y = active_char.pos
    queue = [(0, y, x)]
    distances = {}

    attacking_spot = None
    attacking_spot_distance = None
    while queue:
        steps, y, x = heapq.heappop(queue)
        pos = (x, y)

        cached_dist = distances.get(pos)
        if cached_dist and cached_dist <= steps:
            continue
        distances[pos] = steps

        if attacking_spot_distance and attacking_spot_distance <= steps:
            break

        # If no enemies are around, check next steps
        for npos in grid.neighbors(pos):
            v = grid[npos]

            if v == '.':
                heapq.heappush(queue, (steps + 1, npos[1], npos[0]))
                continue

            if v in ['#', active_char.type]:
                continue

            if v == enemy_type:
                attacking_spot = safe_min(attacking_spot, (y, x))
                attacking_spot_distance = steps

    if attacking_spot:
        y, x = attacking_spot
        return (x, y)

    return None


def move_to_target(grid, active_char, characters):
    attacking_spot = find_attacking_spot(grid, active_char, characters)
    if attacking_spot is None:
        return

    def heuristic(steps, pos):
        return steps + pos_distance(pos, attacking_spot)

    next_steps = []
    for next_step in grid.neighbors(active_char.pos):
        if grid[next_step] != '.':
            continue

        queue = [
            (heuristic(0, next_step), 0, next_step[1], next_step[0])
        ]
        distances = {}
        min_steps = None
        while queue:
            h, steps, y, x = heapq.heappop(queue)
            pos = (x, y)

            cached_dist = distances.get(pos)
            if cached_dist and cached_dist <= steps:
                continue
            distances[pos] = steps

            if pos == attacking_spot:
                min_steps = safe_min(min_steps, steps)

            if min_steps and min_steps <= h:
                break

            for npos in grid.neighbors(pos):
                if grid[npos] == '.':
                    heapq.heappush(
                        queue,
                        (heuristic(steps, npos), steps + 1, npos[1], npos[0])
                    )

        if min_steps is not None:
            heapq.heappush(
                next_steps,
                (min_steps, next_step[1], next_step[0], next_step),
            )

    next_step = heapq.heappop(next_steps)[3]

    print_move(grid, characters, active_char, next_step)

    grid[active_char.pos] = '.'
    active_char.pos = next_step
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
            key=lambda char: (char.health, char.pos[1], char.pos[0]),
            default=None,
        )

    def attack_target(active_char, target):
        print_attack(grid, characters, active_char, target)

        target.health -= active_char.attack
        target.health = max(0, target.health)

        if not target.is_dead:
            return

        grid[target.pos] = '.'
        target_idx = [
            idx
            for idx, char in enumerate(characters)
            if char.id == target.id
        ][0]
        characters.pop(target_idx)

    def key_positions():
        return tuple([
            char.pos
            for char in sorted(characters, key=lambda char: char.id)
        ])

    for active_char in sorted(characters, key=turn_order_key):
        if active_char.is_dead:
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

        move_to_target(grid, active_char, characters)

        target = find_adjacent_target(active_char, enemies)
        if target is not None:
            attack_target(active_char, target)

    return False


def run_game(grid, characters, attack_boost):
    grid = grid.copy()
    characters = [
        char.copy()
        for char in characters
    ]

    elves = [
        char
        for char in characters
        if char.type == 'E'
    ]
    for elf in elves:
        elf.attack += attack_boost

    for full_rounds in range(100000000):
        if DEBUG_ROUNDS:
            print(f'Round: {full_rounds}')

        finished = play_round(grid, characters)
        if attack_boost and any(elf.is_dead for elf in elves):
            return None

        if finished:
            break

    total_health = sum(
        char.health
        for char in characters
    )
    return full_rounds * total_health

def run(problem, lines):
    grid, characters = parse_lines(lines)

    if problem == 1:
        return run_game(grid, characters, attack_boost=0)

    for attack_boost in range(1, 100000):
        outcome = run_game(grid, characters, attack_boost=attack_boost)
        if outcome is not None:
            return outcome

example1 = multiline_lines(r"""
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######
""")

example2 = multiline_lines(r"""
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
""")

example3 = multiline_lines(r"""
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
""")

example4 = multiline_lines(r"""
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######
""")

example5 = multiline_lines(r"""
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######
""")

example6 = multiline_lines(r"""
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

run(1, example1) | eq(36334)
run(1, example2) | eq(27730)
run(1, example3) | eq(39514)
run(1, example4) | eq(27755)
run(1, example5) | eq(28944)
run(1, example6) | eq(18740)

run(1, input_lines) | debug('Star 1') | eq(198531)

run(2, example2) | eq(4988)
run(2, example3) | eq(31284)
run(2, example4) | eq(3478)
run(2, example5) | eq(6474)
run(2, example6) | eq(1140)

run(2, input_lines) | debug('Star 2') | eq(90420)
