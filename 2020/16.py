from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

FIELDS = 0
MY_TICKET = 1
OTHER_TICKETS = 2

def is_valid(value, fields):
    for field, ranges in fields.items():
        for (v0, v1) in ranges:
            if v0 <= value <= v1:
                return True
    return False

def find_errors(fields, tickets):
    return sum([
        value
        for ticket in tickets
        for value in ticket
        if not is_valid(value, fields)
    ])

def get_ticket_field_masks(value, fields):
    mask = 0
    for i, (field, ranges) in enumerate(fields.items()):
        bit = 1 << i
        for (v0, v1) in ranges:
            if v0 <= value <= v1:
                return True
    return False

def run(lines, problem):
    op = FIELDS

    fields = {}
    my_ticket = None
    other_tickets = []

    for line in lines:
        if not line:
            continue
        if line == 'your ticket:':
            op = MY_TICKET
            continue
        elif line == 'nearby tickets:':
            op = OTHER_TICKETS
            continue

        if op == FIELDS:
            (info, ranges) = line.split(': ')
            ranges = ranges.split(' or ')
            ranges = [
                (int(values[0]), int(values[1]))
                for range_values in ranges
                if (values := range_values.split('-'))
            ]
            fields[info] = ranges
        elif op == MY_TICKET:
            my_ticket = split_comma_ints(line)
        else:
            other_tickets.append(split_comma_ints(line))

    if problem == 1:
        return find_errors(fields, other_tickets)

    mask = (1 << len(fields)) - 1
    valid_tickets = [
        ticket
        for ticket in tickets
        for value in ticket
        if not is_valid(value, fields)
    ]


example1 = multiline_lines(r"""
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
""")

run(example1, 1) | eq(71)
run(input_lines, 1) | debug('Star 1') | eq(26941)

run(input_lines, 2) | debug('Star 2')
