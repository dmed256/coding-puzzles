import hashlib
from advent_of_code import *

def is_nice(s):
    vowel_count = 0
    prev_c = None
    has_pair = False
    for c in s:
        pair = f'{prev_c}{c}'
        if pair in ['ab', 'cd', 'pq', 'xy']:
            return False

        if c in 'aeiou':
            vowel_count += 1

        has_pair = has_pair or (prev_c == c)
        prev_c = c

    return has_pair and vowel_count >= 3

def run(s):
    nice_count = 0
    for line in s.splitlines():
        if is_nice(line.strip()):
            nice_count += 1
    return nice_count

run('ugknbfddgicrmopn') | eq(1)
run('aaa') | eq(1)
run('jchzalrnumimnmhp') | eq(0)
run('haegwjzuvuyypxyu') | eq(0)
run('dvszwmarrgswjxmb') | eq(0)

test_input = get_input()

run(test_input) | debug('Star 1')


def is_nice2(s):
    pairs = []
    prev_c = None
    prev_prev_c = None

    has_sandwich = False
    for c in s:
        if prev_prev_c == c:
            has_sandwich = True

        pairs.append(f'{prev_c}{c}')
        prev_prev_c = prev_c
        prev_c = c

    if not has_sandwich:
        return False

    for i, p1 in enumerate(pairs):
        for p2 in pairs[i+2:]:
            if p1 == p2:
                return True

    return False

def run2(s):
    nice_count = 0
    for line in s.splitlines():
        if is_nice2(line.strip()):
            nice_count += 1
    return nice_count

run2('aaa') | eq(0)
run2('qjhvhtzxzqqjkmpb') | eq(1)
run2('xxyxx') | eq(1)
run2('uurcxstgmygtbstg') | eq(0)
run2('ieodomkazucvgmuy') | eq(0)

# 63
run2(test_input) | debug('Star 2')