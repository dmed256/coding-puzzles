from repo_utils import *
from utils import *

input_value = get_input()
input_lines = get_input_lines()

def run(lines, chars):
    values = list(range(chars))
    lengths = [int(x) for x in lines[0].split(',')]

    values = knot_hash_values(values, lengths, 1)
    return values[0] * values[1]

def run2(content):
    return get_knot_hash(content)

example1 = multiline_lines(r"""
3,4,1,5
""")

run(example1, 5) | eq(12)

run(input_lines, 256) | debug('Star 1') | eq(8536)

run2('') | eq('a2582a3a0e66e6e86e3812dcb672a272')
run2('AoC 2017') | eq('33efeb34ea91902bb2f59c9920caa6cd')
run2('1,2,3') | eq('3efbe78a8d82f29979031a4aa0b16a9d')
run2('1,2,4') | eq('63960835bcdc130f0b66d7ff4f6a5a8e')

run2(input_lines) | debug('Star 2') | eq('aff593797989d665349efe11bb4fd99b')
