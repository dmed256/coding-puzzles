import re
from advent_of_code import *

def get_orbits(lines):
    orbits = {}
    planets = set()
    for line in lines:
        [a, b] = line.split(')')
        orbits[a] = orbits.get(a, set())
        orbits[a].add(b)
        planets.add(a)
        planets.add(b)
    return [orbits, planets]

def get_orbit_counts(lines):
    [orbits, planets] = get_orbits(lines)

    direct_orbits = {
        p: len(orbits.get(p, set()))
        for p in planets
    }

    indirect_orbits = {}
    while len(indirect_orbits) < len(planets):
        has_indirect_orbits = set(indirect_orbits.keys())
        needs_indirect_orbits = planets - has_indirect_orbits

        for planet in needs_indirect_orbits:
            planet_orbits = orbits.get(planet, set())
            if planet_orbits <= set(indirect_orbits.keys()):
                indirect_orbits[planet] = sum(
                    direct_orbits[p2]
                    for p2 in planet_orbits
                ) + sum(
                    indirect_orbits[p2]
                    for p2 in planet_orbits
                )

    return [
        sum(direct_orbits.values()),
        sum(indirect_orbits.values()),
    ]

def run(lines):
    [d, i] = get_orbit_counts(lines)
    return d + i

example = multiline_lines(r"""
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
""")

get_orbit_counts(example) | eq([11, 31])

input_lines = get_input_lines()

run(input_lines) | debug('Star 1')

def get_node_path(inverse_orbits, node):
    path = [[node, 0]]
    while True:
        [last_node, distance] = path[-1]
        if last_node == 'COM':
            break
        path.append([inverse_orbits[last_node], distance + 1])

    return {
        node: distance
        for [node, distance] in path
    }

def run2(lines):
    [orbits, planets] = get_orbits(lines)

    inverse_orbits = {'COM': None}
    for p1, orbited_planets in orbits.items():
        for p2 in orbited_planets:
            inverse_orbits[p2] = p1

    you_path = get_node_path(inverse_orbits, 'YOU')
    san_path = get_node_path(inverse_orbits, 'SAN')

    you_path_nodes = set(you_path.keys())
    san_path_nodes = set(san_path.keys())

    same_nodes = you_path_nodes & san_path_nodes

    return min(
        you_path[p] + san_path[p]
        for p in same_nodes
    ) - 2

example = multiline_lines(r"""
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN
""")

run2(example) | eq(4)

run2(input_lines) | debug('Star 2')
