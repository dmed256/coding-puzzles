from advent_of_code import *
from int_processor import *

input_value = get_input()
p = IntProcessor(input_value)

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
        left = [0, 0, 0, 3]

        for i in range(100):
            prev_x = left[-1]
            y = len(left)

            x = prev_x
            while True:
                if get_output(x, y):
                    break
                x += 1
            left.append(x)


        while True:
            prev_x1 = left[-1]
            y1 = len(left)

            x1 = prev_x1
            while True:
                if get_output(x1, y1):
                    break
                x1 += 1
            left.append(x1)

            if get_output(x1 + 99, y1 - 99):
                break

        min_y = len(left) - 100
        min_x = left[-1]
        return min_y + (10000 * min_x)

Problem1().run() | debug('Star 1') | eq(211)

Problem2().run() | debug('Star 2') | eq(8071006)
