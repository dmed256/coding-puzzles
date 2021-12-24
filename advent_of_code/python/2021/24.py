from repo_utils import *


# Python was too slow so I had to code it up with C++ first to make sure
# my solution was right...
def solve(inputs, input_index, init_z, model_number, w_order, cache):
    key = (
        (abs(init_z) * 100)
        + (init_z < 0) * 10
        + input_index
    )
    if key in cache:
        return None
    cache.add(key)

    if len(inputs) <= input_index:
        return None if init_z else model_number

    a, b, c = inputs[input_index]

    for w in w_order:
        z = init_z

        x = w != ((z % 26) + b)
        z //= a

        z *= (25 * x) + 1
        z += (w + c) * x

        value = solve(
            inputs,
            input_index + 1,
            z,
            (model_number * 10) + w,
            w_order,
            cache,
        )
        if value is not None:
            return value

    return None


def run():
    inputs = (
        (1, 11, 6),
        (1, 13, 14),
        (1, 15, 14),
        (26, -8, 10),
        (1, 13, 9),
        (1, 15, 12),
        (26, -11, 8),
        (26, -4, 13),
        (26, -15, 12),
        (1, 14, 6),
        (1, 14, 9),
        (26, -1, 15),
        (26, -8, 4),
        (26, -14, 1),
    )

    min_order = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    max_order = (9, 8, 7, 6, 5, 4, 3, 2, 1)

    max_value = solve(inputs, 0, 0, 0, max_order, set())
    min_value = solve(inputs, 0, 0, 0, min_order, set())

    return min_value, max_value

min_value, max_value = run()

max_value | debug('Star 1') | eq(99394899891971)
min_value | debug('Star 2') | eq(92171126131911)
