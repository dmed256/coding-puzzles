from advent_of_code import *
from int_processor import *

input_value = get_input()
p = IntProcessor(input_value, SINGLE_LOOP_MODE)

def get_output(x, y):
    [value] = p.run(inputs=[x, y])
    return value

def get_row_output(y, prev_row):
    [prev_x1, prev_x2] = prev_row

    has_x1 = False
    for x1 in range(prev_x1, prev_x2 + 10):
        if get_output(x1, y):
            has_x1 = True
            break

    if not has_x1:
        return []

    x2 = max(prev_x2, x1)
    while True:
        if not get_output(x2, y):
            break
        x2 += 1

    return [x1, x2 - 1]


class Problem1:
    def run(self):
        count = 0
        prev_row = [0, 0]
        for y in range(0, 50):
            row = get_row_output(y, prev_row)
            if row:
                count += 1 + row[1] - row[0]
                prev_row = row

        return count

class Problem2:
    def run(self):
        rows = [[0, 0], [0, 0], [0, 0], [3, 3]]
        while True:
            [prev_x1, prev_x2] = rows[-1]
            y = len(rows)

            has_x1 = False
            for x1 in range(prev_x1, prev_x2 + 5):
                if get_output(x1, y):
                    has_x1 = True
                    break

            if not has_x1:
                rows.apped


            x2 = prev_x2
            while True:
                if not get_output(x2, y):
                    break
                x2 += 1

            rows.append([x1, x2])

            if y < 99:
                continue

            prev_y = y - 99
            [prev_x1, prev_x2] = rows[prev_y]
            if prev_x2 - x1 >= 100:
                break

        if True:
            for y in range(prev_y, prev_y + 100):
                for x in range(x1, x1 + 100):
                    if not get_output(x, y):
                        raise Exception(f"({x1}, {prev_y}) -> ({x}, {y}) not valid")

        return prev_y + (10000 * x1)

Problem1().run() | debug('Star 1')

Problem2().run() | debug('Star 2')
