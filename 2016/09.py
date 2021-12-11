from advent_of_code import *

input_lines = get_input_lines()

def run(problem, value):
    parts = [
        part.strip()
        for part in re.split('(\([^)]+\))', value)
        if part.strip()
    ]

    def decompress(value):
        if problem == 1:
            return len(value)

        if '(' not in stack:
            return len(value)

        return run(problem, value)

    ans = 0
    stack = ''
    marker = None
    for part in parts:
        if marker is None and part.startswith('('):
            chars, times = part[1:-1].split('x')
            marker = (int(chars), int(times))
            continue

        if marker is None:
            ans += len(part)
            continue

        chars, times = marker
        stack += part

        if len(stack) < chars:
            continue

        repeated_part = stack[:chars]
        tail_length = len(stack) - chars

        ans += times * decompress(repeated_part)
        ans += tail_length

        stack = ''
        marker = None

    if stack:
        ans += len(stack)

    return ans

run(1, 'ADVENT') | eq(6)
run(1, 'A(1x5)BC') | eq(7)
run(1, '(3x3)XYZ') | eq(9)
run(1, 'A(2x2)BCD(2x2)EFG') | eq(11)
run(1, '(6x1)(1x3)A') | eq(6)
run(1, 'X(8x2)(3x3)ABCY') | eq(18)

run(1, input_lines[0]) | debug('Star 1') | eq(150914)

run(2, '(3x3)XYZ') | eq(9)
run(2, 'X(8x2)(3x3)ABCY') | eq(20)
run(2, '(27x12)(20x12)(13x14)(7x10)(1x12)A') | eq(241920)
run(2, '(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN') | eq(445)

run(2, input_lines[0]) | debug('Star 2') | eq(11052855125)
