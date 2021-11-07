from advent_of_code import *

def run(s):
    area = 0
    for line in s.splitlines():
        [x, y, z] = line.strip().split('x')
        [x, y, z] = [int(x), int(y), int(z)]

        padding = min(x*y, x*z, y*z)
        area += (
            2*x*y
            + 2*x*z
            + 2*y*z
            + padding
        )
    return area

run('2x3x4') | eq(58)
run('1x1x10') | eq(43)

test_input = get_input()

run(test_input) | debug('Star 1')


def run2(s):
    ribbon = 0
    for line in s.splitlines():
        [x, y, z] = line.strip().split('x')
        [x, y, z] = [int(x), int(y), int(z)]

        per = 2*x + 2*y + 2*z - 2*max(x, y, z)
        ribbon += per + (x * y * z)

    return ribbon

run2('2x3x4') | eq(34)
run2('1x1x10') | eq(14)

run2(test_input) | debug('Star 2')
