from repo_utils import *

open_chars = 'bcdef'

def run(problem, start_value):
    grid = Grid([
        [0 for c in range(4)]
        for r in range(4)
    ])

    queue = [(start_value, (0, 0))]
    last_path = ''

    while queue:
        value, pos = queue.pop(0)

        up, down, left, right = md5(value)[:4]

        next_directions = []
        if up in open_chars:
            next_directions.append((GRID_UP, 'U'))
        if down in open_chars:
            next_directions.append((GRID_DOWN, 'D'))
        if left in open_chars:
            next_directions.append((GRID_LEFT, 'L'))
        if right in open_chars:
            next_directions.append((GRID_RIGHT, 'R'))

        for direction, letter in next_directions:
            next_pos = grid.apply_direction(pos, direction)
            if next_pos is None:
                continue

            next_value = value + letter
            if next_pos == (3, 3):
                path = next_value[len(start_value):]
                if problem == 1:
                    return path

                last_path = path
            else:
                queue.append((next_value, next_pos))

    return len(last_path)

run(1, 'ihgpwlah') | eq('DDRRRD')
run(1, 'kglvqrro') | eq('DDUDRLRRUDRD')
run(1, 'ulqzkmiv') | eq('DRURDRUDDLLDLUURRDULRLDUUDDDRR')

run(1, 'qtetzkpl') | debug('Star 1') | clipboard()

run(2, 'ihgpwlah') | eq(370)
run(2, 'kglvqrro') | eq(492)
run(2, 'ulqzkmiv') | eq(830)

run(2, 'qtetzkpl') | debug('Star 2') | clipboard()
