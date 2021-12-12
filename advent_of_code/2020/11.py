from repo_utils import *

input_value = get_input()
input_lines = get_input_lines()

def run(lines, problem):
    grid = Grid(lines)
    seats = {
        pos
        for pos, v in grid
        if v == 'L'
    }
    empty_seats = seats.copy()
    filled_seats = set()

    neighbors = {}
    for pos in seats:
        if problem == 1:
            neighbors[pos] = [
                pos2
                for direction in DIAG_DIRECTIONS
                if (pos2 := grid.apply_direction(pos, direction))
                and pos2 in seats
            ]
        else:
            neighbors[pos] = []
            for direction in DIAG_DIRECTIONS:
                pos2 = pos
                while pos2 := grid.apply_direction(pos2, direction):
                    if pos2 in seats:
                        neighbors[pos].append(pos2)
                        break

    seats_to_empty = (
        4
        if problem == 1 else
        5
    )

    def find_adj_filled(filled_seats, pos):
        return len([
            1
            for neighbor in neighbors[pos]
            if neighbor in filled_seats
        ])

    changed = True
    while changed:
        changed = False
        filled_seats_copy = filled_seats.copy()
        empty_seats_copy = empty_seats.copy()

        for pos in empty_seats_copy:
            if find_adj_filled(filled_seats_copy, pos) == 0:
                changed = True
                filled_seats.add(pos)
                empty_seats.remove(pos)

        for pos in filled_seats_copy:
            if find_adj_filled(filled_seats_copy, pos) >= seats_to_empty:
                changed = True
                filled_seats.remove(pos)
                empty_seats.add(pos)

    return len(filled_seats)

example1 = multiline_lines(r"""
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
""")

run(example1, 1) | eq(37)
run(input_lines, 1) | debug('Star 1') | eq(2299)

run(example1, 2) | eq(26)
run(input_lines, 2) | debug('Star 2') | eq(2047)
