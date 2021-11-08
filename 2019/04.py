import re
from advent_of_code import *

def is_password(value):
    value = str(value)
    if len(value) != 6:
        return False

    has_pair = False
    for i in range(5):
        if value[i] > value[i + 1]:
            return False
        has_pair |= value[i] == value[i + 1]

    return has_pair

example1 = 111111
example2 = 223450
example3 = 123789

is_password(example1) | eq(True)
is_password(example2) | eq(False)
is_password(example3) | eq(False)

def run():
    return len([
        i
        for i in range(178416, 676461 + 1)
        if is_password(i)
    ])

run() | debug('Star 1') | eq(1650)

def is_password2(value):
    if not is_password(value):
        return False

    pairs = [
        num
        for num in re.split('(0+|1+|2+|3+|4+|5+|6+|7+|8+|9+)', str(value))
        if len(num) == 2
    ]
    return len(pairs) > 0

example1 = 112233
example2 = 123444
example3 = 111122

is_password2(example1) | eq(True)
is_password2(example2) | eq(False)
is_password2(example3) | eq(True)

def run2():
    return len([
        i
        for i in range(178416, 676461 + 1)
        if is_password2(i)
    ])

run2() | debug('Star 2') | eq(1129)