from advent_of_code import *

# @testable
# def run(lines):
#     l = [0 for i in range(1000 * 1000)]

#     for line in lines:
#         words = line.split(' ')
#         [x1, y1] = words[-3].split(',')
#         [x1, y1] = [int(x1), int(y1)]

#         [x2, y2] = words[-1].split(',')
#         [x2, y2] = [int(x2), int(y2)]

#         if line.startswith('turn on '):
#             value = 1
#         elif line.startswith('toggle '):
#             value = None
#         elif line.startswith('turn off '):
#             value = 0

#         if value is not None:
#             for y in range(y1, y2 + 1):
#                 for x in range(x1, x2 + 1):
#                     l[x + 1000*y] = value
#         else:
#             for y in range(y1, y2 + 1):
#                 for x in range(x1, x2 + 1):
#                     l[x + 1000*y] = (l[x + 1000*y] + 1) % 2

#     return sum(l)

# run(['turn on 0,0 through 999,999']).should_be(1000 * 1000)
# run(['toggle 0,0 through 999,0']).should_be(1000)
# run(['turn off 499,499 through 500,500']).should_be(0)

# input_lines = get_input_lines()

# run(input_lines).debug('Star 1')


@testable
def run2(lines):
    l = [0 for i in range(1000 * 1000)]

    for line in lines:
        words = line.split(' ')
        [x1, y1] = words[-3].split(',')
        [x1, y1] = [int(x1), int(y1)]

        [x2, y2] = words[-1].split(',')
        [x2, y2] = [int(x2), int(y2)]

        if line.startswith('turn on '):
            value = 1
        elif line.startswith('toggle '):
            value = 2
        elif line.startswith('turn off '):
            value = -1

        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                l[x + 1000*y] = max(0, l[x + 1000*y] + value)

    return sum(l)

run2(['turn on 0,0 through 0,0']).should_be(1)
run2(['toggle 0,0 through 999,999']).should_be(2000000)

input_lines = get_input_lines()

# 17325717 - Too low
run2(input_lines).debug('Star 2')
