from advent_of_code import *
import json

# NOTE: NOT DONE!

def run(value):
    v = json.loads(value)

run('[1,2,3]') | eq()
run('[[[3]]]') | eq()
run('{"a": [-1,1]}') | eq(0)
run('[-1, {"a":1}]') | eq(0)
run('[]') | eq(0)
run('{}') | eq(0)

input_value = get_input()

run(input_value) | debug('Star 1')
