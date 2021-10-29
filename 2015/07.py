from advent_of_code import *

max_16bit_value = sum((
    1 << bit
    for bit in range(16)
))

def get_value(signals, key):
    if key.isdigit():
        return int(key)

    return signals.get(key)

def get_wire_value(signals, line):
    [instruction, wire] = line.split(' -> ')

    if wire in signals:
        return [wire, signals[wire]]

    instruction_words = instruction.split(' ')

    if len(instruction_words) == 1:
        value = get_value(signals, instruction)
    elif instruction.startswith('NOT '):
        not_value = get_value(
            signals,
            instruction.replace('NOT ', ''),
        )
        if not_value is None:
            return [wire, None]
        value = ~not_value
    else:
        for op in ['AND', 'OR', 'LSHIFT', 'RSHIFT']:
            if op in instruction:
                break
        [left, right] = instruction.split(f' {op} ')
        left = get_value(signals, left)
        right = get_value(signals, right)
        if left is None or right is None:
            return [wire, None]
        if op == 'AND':
            value = left & right
        elif op == 'OR':
            value = left | right
        elif op == 'LSHIFT':
            value = left << right
        elif op == 'RSHIFT':
            value = left >> right

    return [wire, value]

@testable
def run(lines, output_wire, default_signals=None):
    signals = default_signals or {}
    definitions = lines
    while len(definitions):
        missing_definitions = []
        for line in lines:
            [wire, value] = get_wire_value(signals, line)
            if value is not None:
                signals[wire] = max_16bit_value & value
            else:
                missing_definitions.append(line)
        definitions = missing_definitions

    return signals[output_wire]

example = multiline_lines("""
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
""")

run(example, 'd').should_be(72)
run(example, 'e').should_be(507)
run(example, 'f').should_be(492)
run(example, 'g').should_be(114)
run(example, 'h').should_be(65412)
run(example, 'i').should_be(65079)
run(example, 'x').should_be(123)
run(example, 'y').should_be(456)

input_lines = get_input_lines()

run(input_lines, 'a').debug('Star 1')

run(input_lines, 'a', {'b': 16076}).debug('Star 2')
