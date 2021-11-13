import itertools
from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

def run(lines, problem):
    graph = {}
    cities = set()
    for line in lines:
        [city_names, distance] = line.split(' = ')
        [c1, c2] = city_names.split(' to ')
        distance = int(distance)
        graph[(c1, c2)] = distance
        graph[(c2, c1)] = distance

        cities.add(c1)
        cities.add(c2)

    def get_distance(order):
        distance = 0
        c1 = order[0]
        for c2 in order[1:]:
            distance += graph[(c1, c2)]
            c1 = c2
        return distance

    distances = (
        get_distance(order)
        for order in itertools.permutations(cities)
    )
    if problem == 1:
        return min(distances)
    else:
        return max(distances)


example1 = multiline_lines(r"""
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
""")

run(example1, 1) | eq(605)

run(input_lines, 1) | debug('Star 1') | eq(117)
run(input_lines, 2) | debug('Star 2') | eq(909)
