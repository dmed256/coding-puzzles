from repo_utils import *

DEBUG_PRINT = False

input_lines = get_input_lines()

amphipod_cost = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}

amphipods = set('ABCD')


def get_grid_positions(grid):
    return tuple(sorted([
        (v, pos)
        for pos, v in grid
        if v in amphipods
    ]))


def get_valid_moves(start_pos, grid, hallway, amphipod_rooms, valid_amphipod_positions):
    amphipod = grid[start_pos]
    room_positions = amphipod_rooms[amphipod]
    in_valid_room = start_pos in room_positions

    if start_pos in hallway:
        valid_positions = set(room_positions)
    else:
        valid_positions = set(valid_amphipod_positions[amphipod])

    # We can't stay still
    if start_pos in valid_positions:
        valid_positions.remove(start_pos)

    invalid_room_residents = {
        grid[room_pos]
        for room_pos in amphipod_rooms[amphipod]
        if grid[room_pos] != '.'
    } - {amphipod}

    # We can only move to rooms that are empty or occupied by
    # the proper amphipods
    if invalid_room_residents:
        valid_positions -= amphipod_rooms[amphipod]

    if not valid_positions:
        return []

    queue = [(0, start_pos)]
    visited_positions = {
        start_pos: 0,
    }
    while queue:
        dist, pos = queue.pop()
        for npos in grid.neighbors(pos):
            if grid[npos] != '.':
                continue

            if npos in visited_positions:
                continue

            visited_positions[npos] = dist + 1
            queue.append((dist + 1, npos))

    next_positions = {
        pos: dist
        for pos, dist in visited_positions.items()
        if pos in valid_positions
    }
    step_cost = amphipod_cost[amphipod]

    moves = []
    for npos, dist in next_positions.items():
        moving_out_of_room = npos not in room_positions

        if in_valid_room:
            # If we're in a room, the only reason to leave is if
            # there are invalid residents in the room
            must_stay_in_room = not bool(invalid_room_residents)

            if moving_out_of_room and must_stay_in_room:
                continue

            # Don't allow moving 1-by-1 inside the room
            # Either stay in the room, go deeper in the room, or go outside of it
            if not moving_out_of_room:
                # If we go down, we should go all the way
                min_empty_room_spot = min([
                    pos[1]
                    for pos in room_positions
                    if grid[pos] == '.'
                ])
                if npos[1] != min_empty_room_spot:
                    continue

        cost = step_cost * dist

        next_grid = grid.copy()
        next_grid[start_pos] = '.'
        next_grid[npos] = amphipod

        moves.append((cost, next_grid))

    return moves


def get_next_grids(grid, positions, hallway, amphipod_rooms, valid_amphipod_positions):
    return [
        move
        for amphipod, pos in positions
        for move in get_valid_moves(
                pos,
                grid,
                hallway,
                amphipod_rooms,
                valid_amphipod_positions,
        )
    ]


def calc_min_cost_left(positions, amphipod_rooms):
    min_cost_left = 0
    for amphipod, pos in positions:
        room_positions = amphipod_rooms[amphipod]

        if pos in room_positions:
            continue

        dist = calc_min_move_dist(pos, room_positions)
        min_cost_left += amphipod_cost[amphipod] * dist

    return min_cost_left


def calc_min_move_dist(pos, room_positions):
    if pos in room_positions:
        return 0

    min_x = min(x for x, y in room_positions)
    min_y = min(y for x, y in room_positions)
    x, y = pos

    hallway_y = min_y - 1

    to_hallway = abs(hallway_y - y)
    to_room_door = abs(min_x - x)
    to_room = 1

    return to_hallway + to_room_door + to_room


def get_queue_entry(cost, grid, positions, amphipod_rooms):
    min_cost_left = calc_min_cost_left(positions, amphipod_rooms)
    return (
        cost + min_cost_left,
        min_cost_left,
        cost,
        positions,
        grid,
    )


def run(problem, lines):
    if problem == 2:
        extra_lines = multiline_lines(r"""
  #D#C#B#A#
  #D#B#A#C#
""")
        lines[3:3] = extra_lines

    grid = Grid(lines, default_value=' ')

    room_x_values = sorted({
        x
        for (x, y), v in grid
        if v in amphipods
    })
    amphipod_rooms = {
        amphipod: {
            pos
            for pos, v in grid
            if pos[0] == room_x and v in amphipods
        }
        for amphipod, room_x in zip('ABCD', room_x_values)
    }
    hallway = {
        pos
        for pos, v in grid
        if v == '.'
        and grid[grid.apply_direction(pos, GRID_DOWN)] == '#'
    }
    valid_amphipod_positions = {
        amphipod: rooms | hallway
        for amphipod, rooms in amphipod_rooms.items()
    }

    positions = get_grid_positions(grid)
    queue = [get_queue_entry(0, grid, positions, amphipod_rooms)]
    min_distances = {}
    while queue:
        min_full_cost, min_cost_left, cost, positions, grid = heapq.heappop(queue)

        if min_cost_left == 0:
            return cost

        min_pos_distance = min_distances.get(positions)
        if min_pos_distance and min_pos_distance < cost:
            continue
        min_distances[positions] = cost

        for move_cost, next_grid in get_next_grids(
                grid,
                positions,
                hallway,
                amphipod_rooms,
                valid_amphipod_positions,
        ):
            next_cost = cost + move_cost
            next_positions = get_grid_positions(next_grid)

            min_pos_distance = min_distances.get(next_positions)
            if min_pos_distance and min_pos_distance <= next_cost:
                continue
            min_distances[next_positions] = next_cost

            heapq.heappush(
                queue,
                get_queue_entry(
                    next_cost,
                    next_grid,
                    next_positions,
                    amphipod_rooms,
                )
            )


example1 = multiline_lines(r"""
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
""")

run(1, example1) | eq(12521)

run(1, input_lines) | debug('Star 1') | eq(17120)

run(2, example1) | eq(44169)

run(2, input_lines) | debug('Star 2') | eq(47234)
