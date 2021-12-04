from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

def parse_input(lines):
    numbers = [int(x) for x in lines[0].split(',')]
    boards = []
    for i in range(2, len(lines), 6):
        boards.append(
            [
                [int(n.strip()) for n in line.split()]
                for line in lines[i:i+5]
                if line.strip()
            ]
        )

    return numbers, boards

def has_bingo(board):
    for c in range(5):
        bingo = True
        for r in range(5):
            if board[c][r] >= 0:
                bingo = False
                break
        if bingo:
            return True

        bingo = True
        for r in range(5):
            if board[r][c] >= 0:
                bingo = False
                break
        if bingo:
            return True

    return False

def board_score(board, called_numbers):
    values = set([
        v if v >= 0 else (-v - 1)
        for row in board
        for v in row
    ])
    max_board = sum(values - set(called_numbers))
    return called_numbers[-1] * max_board

def run(lines, problem):
    numbers, boards = parse_input(lines)

    winning_board = None
    losing_board = None

    called_numbers = []
    for i in range(len(numbers)):
        called_number = numbers[i]
        called_numbers.append(called_number)

        for board in boards:
            for c in range(5):
                for r in range(5):
                    if board[c][r] == called_number and board[c][r] >= 0:
                        board[c][r] = -board[c][r] - 1

        prev_boards = boards
        boards = [
            board
            for board in boards
            if not has_bingo(board)
        ]

        if winning_board is None and len(prev_boards) != len(boards):
            winning_called_numbers = deepcopy(called_numbers)
            winning_board = [
                board
                for board in prev_boards
                if has_bingo(board)
            ][0]

        if len(boards) == 0:
            losing_called_numbers = deepcopy(called_numbers)
            losing_board = prev_boards[0]
            break

    if problem == 1:
        return board_score(winning_board, winning_called_numbers)
    else:
        return board_score(losing_board, losing_called_numbers)

example1 = multiline_lines(r"""
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
""")

run(example1, 1) | eq(4512)

run(input_lines, 1) | debug('Star 1') | eq(16674)

run(example1, 2) | eq(1924)

run(input_lines, 2) | debug('Star 2') | eq(7075)
