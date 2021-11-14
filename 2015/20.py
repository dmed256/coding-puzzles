import math
import sympy

from advent_of_code import *

def run(presents, problem):
    if problem == 1:
        def has_enough_presents(groups):
            group_presents = 10 * sum(groups)
            return group_presents >= presents
    else:
        def has_enough_presents(groups):
            house = max(groups)
            group_presents = 11 * sum((
                g
                for g in groups
                if (g * 50) >= house
            ))
            return group_presents >= presents

    def get_next_prime_count(primes, groups):
        if has_enough_presents(groups):
            return []

        [p, *primes] = primes

        possibilities = []

        value = 1
        for i in range(1, 20):
            value *= p

            new_entries = set()
            for g in groups:
                new_entries.add(g * p)
            groups.update(new_entries)

            if has_enough_presents(groups):
                possibilities.append(value)
                break

            possibilities.extend([
                value * tail
                for tail in get_next_prime_count(primes, groups.copy())
            ])

        return possibilities

    def get_possibilities():
        primes = get_primes(50)
        return get_next_prime_count(primes, {1})

    return min(get_possibilities())

run(60, 1) | eq(4)
run(70, 1) | eq(4)
run(120, 1) | eq(6)
run(36000000, 1) | debug('Star 1') | eq(831600)

# Too high: 1058400
# Too high:  887040
# Too low:   776160
run(36000000, 2) | debug('Star 2')
