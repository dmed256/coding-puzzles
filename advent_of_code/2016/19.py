from repo_utils import *

def run1(value):
    values = [i + 1 for i in range(value)]
    while len(values) > 1:
        next_values = values[::2]

        if len(values) == 1:
            break

        if len(values) % 2:
            next_values.pop(0)

        values = next_values

    return values[0]

def run2(value):
    values = [i + 1 for i in range(value)]
    taker = 0
    while len(values) > 1:
        elfs = len(values)
        stolen = (taker + (elfs // 2)) % elfs

        values.pop(stolen)

        taker += 1
        if elfs <= taker:
            taker = 0

    return values[0]

run1(5) | eq(3)

run1(3018458) | debug('Star 1') | eq(1842613)

run2(5) | eq(2)

# run2(3018458) | submit(2)
