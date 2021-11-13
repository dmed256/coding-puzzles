import math
from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

def parse_lines(lines):
    timestamp = int(lines[0])
    bus_ids = [
        int(x)
        for x in lines[1].split(',')
        if x.isdigit()
    ]
    return (timestamp, bus_ids)

def run(lines):
    (timestamp, bus_ids) = parse_lines(lines)
    (depart, bus_id) = min(
        (bus_id * math.ceil(timestamp / bus_id), bus_id)
        for bus_id in bus_ids
    )
    return (depart - timestamp) * bus_id

example1 = multiline_lines(r"""
939
7,13,x,x,59,x,31,19
""")

run(example1) | eq(295)

run(input_lines) | debug('Star 1') | eq(156)

def run2(lines):
    schedule = lines[1].split(',')
    bus_info = [
        (int(bus_id), offset)
        for offset, bus_id in enumerate(schedule)
        if bus_id.isdigit()
    ]

    t = 0 (mod 7)
    t = 12 (mod 13)
    t = 55 (mod 59)
    t = 25 (mod 31)
    t = 12 (mod 19)



  - OUTPUT:   [[(7, 0), (13, 1), (59, 4), (31, 6), (19, 7)]]
  - EXPECTED: [1068781]

    return bus_info

run2(['', '7,13,x,x,59,x,31,19']) | eq(1068781)
run2(['', '17,x,13,19']) | eq(3417)
run2(['', '67,7,59,61']) | eq(754018)
run2(['', '67,x,7,59,61']) | eq(779210)
run2(['', '67,7,x,59,61']) | eq(1261476)
run2(['', '1789,37,47,1889']) | eq(1202161486)

run2(input_lines) | debug('Star 2')
