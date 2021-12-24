from repo_utils import *

def run(disks):
    t = 1
    while True:
        found = all(
            0 == (shift + t + i + 1) % positions
            for i, (positions, shift) in enumerate(disks)
        )
        if found:
            return t
        t += 1

example1 = [
    (5, 4),
    (2, 1),
]

input_values = [
    (17, 5),
    (19, 8),
    (7, 1),
    (13, 7),
    (5, 1),
    (3, 0),
]

input_values2 = [
    (17, 5),
    (19, 8),
    (7, 1),
    (13, 7),
    (5, 1),
    (3, 0),
    (11, 0),
]

run(example1) | eq(5)

run(input_values) | debug('Star 1') | eq(16824)

run(input_values2) | debug('Star 2') | eq(3543984)
