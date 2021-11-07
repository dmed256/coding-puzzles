from advent_of_code import *

def split(value):
    return [ord(c) - ord('a') for c in value]

def unsplit(value):
    return ''.join([
        chr(ord('a') + v) for v in value
    ])

invalid = set(split('iol'))

def is_valid(value):
    has_straight = False
    for i in range(6):
        v = value[i]
        if (value[i + 1] == v + 1 and
            value[i + 2] == v + 2):
            has_straight = True

    if not has_straight:
        return False

    for v in value:
        if v in invalid:
            return False

    prev_c = None
    count = 0
    pairs = 0
    for c in value:
        if prev_c != c:
            prev_c = c
            pairs += count // 2
            count = 1
        else:
            count += 1
    pairs += count // 2

    return pairs >= 2

def inc(value):
    value2 = value.copy()
    value2[7] += 1
    for i in range(7, 0, -1):
        if value2[i] // 26:
            value2[i - 1] += value2[i] // 26
            value2[i] %= 26
        else:
            break
    return value2

def next_password(value):
    value = inc(split(value))
    while not is_valid(value):
        value = inc(value)

    return unsplit(value)

is_valid(split('hijklmmn')) | eq(False)
is_valid(split('abbceffg')) | eq(False)
is_valid(split('abbcegjk')) | eq(False)
is_valid(split('abcdffaa')) | eq(True)
is_valid(split('ghjaabcc')) | eq(True)

unsplit(inc(split('aaaaaaaa'))) | eq('aaaaaaab')
unsplit(inc(split('aaaaaaaz'))) | eq('aaaaaaba')

next_password('abcdefgh') | eq('abcdffaa')
next_password('ghijklmn') | eq('ghjaabcc')
p1 = next_password('vzbxkghb') | debug('Star 1')
next_password(p1) | debug('Star 2')
