from repo_utils import *

input_lines = get_input_lines()

class Character(BaseModel):
    x: int
    y: int
    type: str
    id: int = 0
    attack: int = 3
    health: int= 200

    @property
    def pos(self):
        return (self.x, self.y)

    def distance_to(self, other):
        return (
            abs(self.x - other.x)
            + abs(self.y - other.y)
        )

enemy_type_map = {
    'G': 'E',
    'E': 'G',
}

def find_target(grid, active_char, enemies):
    enemy_positions = {
        char.pos: char
        for char in enemies
    }

    queue = [(0, active_char.y, active_char.x, None, None, None, None)]
    visited = set()
    target_info = None
    while queue:
        steps, y, x, _, _, next_step_y, next_step_x = heapq.heappop(queue)
        pos = (x, y)

        if pos in enemy_positions:
            target_info = (
                steps,
                pos,
                (next_step_x, next_step_y)
            )
            break

        for npos in grid.neighbors(pos):
            if npos in visited:
                continue
            visited.add(npos)

            v = grid[npos]
            nx, ny = npos

            if next_step_y is None:
                next_step_x = nx
                next_step_y = ny

            if v in ['#', active_char.type]:
                continue

            heapq.heappush(
                queue,
                (
                    steps + 1,
                    ny,
                    nx,
                    y,
                    x,
                    next_step_y,
                    next_step_x,
                 )
            )

    if not target_info:
        return None, None

    _, target_pos, next_step_pos = target_info

    if next_step_pos == active_char.pos:
        next_step_pos = None

    target_char = enemy_positions[target_pos]

    return target_char, next_step_pos

def run(problem, lines):
    grid = Grid(lines)

    def print_state(full_rounds):
        grid.print()
        for char in characters:
            print(char)

        print(f'Round: {full_rounds}')

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

    for full_rounds in range(100000000):
        characters = sorted([
            char
            for char in characters
            if 0 < char.health
        ], key=lambda char: (char.y, char.x))

        for active_char in list(characters):
            if active_char.health <= 0:
                continue

            enemies = [
                char
                for char in characters
                if char.type != active_char.type
            ]

            # We finished the game!
            if not enemies:
                print_state(full_rounds)
                total_health = sum(
                    char.health
                    for char in characters
                )
                return total_health * full_rounds

            # First find the target we're aiming for
            target, next_step = find_target(
                grid,
                active_char,
                enemies,
            )

            # No way to move or attack
            if not target:
                continue

            # Move towards a unit
            if 1 < active_char.distance_to(target):
                grid[active_char.pos] = '.'
                grid[next_step] = active_char.type

                active_char.x = next_step[0]
                active_char.y = next_step[1]

            # Target isn't adjacent
            if 1 < active_char.distance_to(target):
                continue

            # Attack!
            target.health -= active_char.attack

            # Target is dead
            if target.health <= 0:
                grid[target.pos] = '.'
                characters = [
                    char
                    for char in characters
                    if 0 < char.health
                ]


example = multiline_lines(r"""
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
""")
#run(1, example) | eq(27730)

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
