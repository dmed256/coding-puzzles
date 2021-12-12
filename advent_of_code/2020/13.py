import math
from repo_utils import *

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
        (bus_id, (bus_id - offset) % bus_id)
        for offset, bus_id_str in enumerate(schedule)
        if bus_id_str.isdigit()
        and (bus_id := int(bus_id_str))
    ]
    # t = t_mod_id[0] (mod bus_id[0])
    # t = t_mod_id[1] (mod bus_id[1])
    # ...
    #
    # ->
    #
    # t = z[0]*t_mod_id[0]*n[0] + z[1]*t_mod_id[1]*n[1] + ...
    #
    # t (mod bus_id[0])
    #
    # -> z[0]*t_mod_id[0]*n[0] + z[1]*t_mod_id[1]*n[1] + ... (mod bus_id[0])
    #
    # -> z[0]*t_mod_id[0]*n[0] (mod bus_id[0])
    #    [Note: n[i] == 0 (mod bus_id[j]) when i != j]
    #
    # -> t_mod_id[0] (mod bus_id[0])
    #    [z[i] == n[i]^-1 (mod bus_id[0])]

    N = 1
    for (bus_id, _) in bus_info:
        N *= bus_id
    n = [
        N // bus_id
        for (bus_id, _) in bus_info
    ]

    return sum(
        t_mod_id * n[i] * inverse_mod(n[i], bus_id)
        for i, (bus_id, t_mod_id) in enumerate(bus_info)
    ) % N

run2(['', '7,13,x,x,59,x,31,19']) | eq(1068781)
run2(['', '17,x,13,19']) | eq(3417)
run2(['', '67,7,59,61']) | eq(754018)
run2(['', '67,x,7,59,61']) | eq(779210)
run2(['', '67,7,x,59,61']) | eq(1261476)
run2(['', '1789,37,47,1889']) | eq(1202161486)

run2(input_lines) | debug('Star 2') | eq(404517869995362)
