import re
from advent_of_code import *

def get_fuel(mass):
    return (mass // 3) - 2

def run(lines):
    fuel = 0
    for line in lines:
        mass = int(line)
        fuel += get_fuel(mass)
    return fuel

example = multiline_lines(r"""
""
"abc"
"aaa\"aaa"
"\x27"
""")

run(['12']) | eq(2)
run(['14']) | eq(2)
run(['1969']) | eq(654)
run(['100756']) | eq(33583)

input_lines = get_input_lines()

run(input_lines) | debug('Star 1')

def run2(lines):
    fuel = 0
    for line in lines:
        mass = int(line)
        while mass > 0:
            mass_fuel = get_fuel(mass)
            if mass_fuel > 0:
                fuel += mass_fuel
            mass = mass_fuel

    return fuel

run2(['14']) | eq(2)
run2(['1969']) | eq(966)
run2(['100756']) | eq(50346)

run2(input_lines) | debug('Star 2')