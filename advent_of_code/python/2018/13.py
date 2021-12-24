from repo_utils import *

input_lines = get_input_lines()

plus_directions = ['L', 'S', 'R']

turn_rotations = {
    '/': {
        GRID_UP: GRID_RIGHT,
        GRID_LEFT: GRID_DOWN,
        GRID_RIGHT: GRID_UP,
        GRID_DOWN: GRID_LEFT,
    },
    '\\': {
        GRID_UP: GRID_LEFT,
        GRID_RIGHT: GRID_DOWN,
        GRID_LEFT: GRID_UP,
        GRID_DOWN: GRID_RIGHT,
    },
}

def run(problem, lines):
    grid = Grid(lines, default_value=' ')

    carts = []
    for cart, direction in zip(
            ['>', '^', '<', 'v'],
            [GRID_RIGHT, GRID_UP, GRID_LEFT, GRID_DOWN],
    ):
        for pos in grid.find_all(cart):
            inv_pos = (pos[1], pos[0])
            heapq.heappush(carts, (inv_pos, direction, 0))

    while 1 < len(carts):
        next_carts = []
        while carts:
            inv_pos, direction, turns = heapq.heappop(carts)
            pos = (inv_pos[1], inv_pos[0])

            pos = grid.apply_direction(pos, direction)
            v = grid[pos]

            if v in turn_rotations:
                direction = turn_rotations[v][direction]
            elif v == '+':
                plus_direction = plus_directions[turns]
                turns = (turns + 1) % 3

                if plus_direction == 'L':
                    direction = GRID_COUNTER_CLOCKWISE[direction]
                elif plus_direction == 'R':
                    direction = GRID_CLOCKWISE[direction]

            inv_pos = (pos[1], pos[0])
            crashed = any(
                other_inv_pos == inv_pos
                for other_inv_pos, _, _ in (carts + next_carts)
            )
            if not crashed:
                heapq.heappush(next_carts, (inv_pos, direction, turns))
                continue

            if problem == 1:
                return f'{pos[0]},{pos[1]}'

            # Remove crashed carts
            carts = [
                cart
                for cart in carts
                if cart[0] != inv_pos
            ]
            next_carts = [
                cart
                for cart in next_carts
                if cart[0] != inv_pos
            ]
            heapq.heapify(carts)
            heapq.heapify(next_carts)

        carts = next_carts

    inv_pos, _, _ = carts[0]
    return f'{inv_pos[1]},{inv_pos[0]}'

example1 = multiline_lines(r"""
/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/
""")

run(1, example1) | eq('7,3')

run(1, input_lines) | debug('Star 1') | eq('83,121')

example2 = multiline_lines(r"""
/>-<\
|   |
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/
""")

run(2, example2) | eq('6,4')

run(2, input_lines) | debug('Star 2') | eq('102,144')
