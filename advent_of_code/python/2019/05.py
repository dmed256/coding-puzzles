from repo_utils import *
from int_processor import *

def run(values, inputs):
    p = IntProcessor(values)
    return p.run(inputs=inputs)

example1 = split_comma_ints('3,0,4,0,99')
for i in range(100):
    run(example1, [i]) | eq([i])

input_value = split_comma_ints(get_input())

run(input_value, [1])[-1] | debug('Star 1') | eq(12428642)

less_than_8 = """
3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99
"""

for i in range(8):
    run(less_than_8, [i])[-1] | eq(999)

run(less_than_8, [8])[-1] | eq(1000)

for i in range(9, 100):
    run(less_than_8, [i])[-1] | eq(1001)

run(input_value, [5])[-1] | debug('Star 2') | eq(918655)
