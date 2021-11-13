from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

FIELDS = 0
MY_TICKET = 1
OTHER_TICKETS = 2

def get_ticket_field_mask(value, fields):
    mask = 0
    for i, (field, ranges) in enumerate(fields.items()):
        bit = 1 << i
        is_valid = bool([
            1
            for (v0, v1) in ranges
            if v0 <= value <= v1
        ])
        if is_valid:
            mask += bit

    return mask

def is_valid_ticket(ticket, fields):
    for value in ticket:
        if not get_ticket_field_mask(value, fields):
            return False
    return True

def find_errors(fields, tickets):
    return sum([
        value
        for ticket in tickets
        for value in ticket
        if not get_ticket_field_mask(value, fields)
    ])

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
        for ticket in [my_ticket, *other_tickets]
        if is_valid_ticket(ticket, fields)
    ]

    field_masks = [mask] * len(fields)
    for ticket in valid_tickets:
        for field, value in enumerate(ticket):
            field_masks[field] &= get_ticket_field_mask(value, fields)

    for mask in field_masks:
        for i in range(len(fields)):
            if mask & (1 << i):
                pass

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
