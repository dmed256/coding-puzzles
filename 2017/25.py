from advent_of_code import *

# 55

input_value = get_input()
input_lines = get_input_lines()

def run():
    state = 'a'

    ptr = 0
    value = set()
    for i in range(12208951):
        if state == 'a':
            if ptr not in value:
                value.add(ptr)
                ptr += 1
                state = 'b'
            else:
                value.remove(ptr)
                ptr -= 1
                state = 'e'
            continue

        if state == 'b':
            if ptr not in value:
                value.add(ptr)
                ptr -= 1
                state = 'c'
            else:
                value.remove(ptr)
                ptr += 1
                state = 'a'
            continue

        if state == 'c':
            if ptr not in value:
                value.add(ptr)
                ptr -= 1
                state = 'd'
            else:
                value.remove(ptr)
                ptr += 1
                state = 'c'
            continue

        if state == 'd':
            if ptr not in value:
                value.add(ptr)
                ptr -= 1
                state = 'e'
            else:
                value.remove(ptr)
                ptr -= 1
                state = 'f'
            continue

        if state == 'e':
            if ptr not in value:
                value.add(ptr)
                ptr -= 1
                state = 'a'
            else:
                ptr -= 1
                state = 'c'
            continue

        if state == 'f':
            if ptr not in value:
                value.add(ptr)
                ptr -= 1
                state = 'e'
            else:
                ptr += 1
                state = 'a'

    return len(value)

run() | debug('Star 1') | eq(4387)
