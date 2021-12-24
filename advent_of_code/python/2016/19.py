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
    get_right = [i + 1 for i in range(value)]
    get_right[-1] = 0

    get_left = [i - 1 for i in range(value)]
    get_left[0] = value - 1

    elfs = value
    taker_ptr = 0
    stolen_ptr = (elfs // 2)
    taker_to_stolen = stolen_ptr

    def get_neighbors(n):
        return get_left[n], get_right[n]

    def delete_node(n):
        left, right = get_neighbors(n)
        get_right[left] = right
        get_left[right] = left
        get_left[n] = ' '
        get_right[n] = ' '
        return right

    while 1 < elfs:
        stolen_ptr = delete_node(stolen_ptr)
        taker_ptr = get_right[taker_ptr]

        taker_to_stolen -= 1
        elfs -= 1

        while taker_to_stolen < (elfs // 2):
            stolen_ptr = get_right[stolen_ptr]
            taker_to_stolen += 1

        while (elfs // 2) < taker_to_stolen:
            stolen_ptr = get_left[stolen_ptr]
            taker_to_stolen -= 1

    return taker_ptr + 1

run1(5) | eq(3)

run1(3018458) | debug('Star 1') | eq(1842613)

run2(5) | eq(2)

run2(3018458) | debug('Star 2') | eq(1424135)
