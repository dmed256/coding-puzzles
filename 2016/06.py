from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

def run(problem, lines):
    chars = len(lines[0])
    counters = [
        defaultdict(int)
        for _ in range(chars)
    ]
    for line in lines:
        for i, c in enumerate(line):
            counters[i][c] += 1

    ans1 = ''
    ans2 = ''
    for counter in counters:
        _, c1 = max((count, c) for c, count in counter.items())
        _, c2 = min((count, c) for c, count in counter.items())
        ans1 += c1
        ans2 += c2

    return ans1 if problem == 1 else ans2

run(1, input_lines) | debug('Star 1') | eq('asvcbhvg')

run(2, input_lines) | debug('Star 2') | eq('odqnikqv')
