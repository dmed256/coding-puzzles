import re
import itertools
from termcolor import colored
from advent_of_code import *
from int_processor import *

example1 = multiline_input("""
109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99
""")
example2 = multiline_input("""
1102,34915192,34915192,7,4,7,99,0
""")
example3 = multiline_input("""
104,1125899906842624,99
""")

def run(values, inputs):
    processor = IntProcessor(values)
    return processor.run(inputs=inputs)

run(example1, []) | eq([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99])

[output] = run(example2, [])
len(str(output)) | eq(16)

run(example3, []) | eq([1125899906842624])

input_value = get_input()

run(input_value, [1]) | debug()
run(input_value, [2]) | debug()
