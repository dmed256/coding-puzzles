import math
import sympy

from advent_of_code import *

def run(presents):
    presents = presents // 10

    prime_cap = math.ceil(math.sqrt(presents))
    primes = get_primes(prime_cap)
    max_primes = {}
    for p in primes:
        pi = p
        for i in range(10000):
            pi *= p
            if pi >= presents:
                max_primes[p] = i
                break

    def get_other_primes(value, max_value, missing_primes):
        [p, *missing_primes] = missing_primes

        possibilities = []
        ps = []
        while value < max_value:
            value *= p
            ps.append(p)
            if value < max_value:
                possibilities.extend([
                    [*ps, *tail]
                    for tail in get_other_primes(value, max_value, missing_primes)
                ])
            else:
                possibilities.append([*ps])

        return possibilities

    possibilities = get_other_primes(1, presents, primes)
    for p in possibilities:
        if p[:4] == [2, 2, 2, 2] and p[4:7] == [3, 3, 3]:
            print(p)
    print([2, 2, 2, 2, 3, 3, 3, 5, 5, 7, 11] in possibilities)
    print([2, 2, 2, 2, 3, 3, 3, 5, 5, 7, 11])

# run(10) | eq(1)
# run(30) | eq(2)
# run(40) | eq(3)
# run(60) | eq(4)
# run(70) | eq(4)
# run(120) | eq(6)
run(36000000) | debug('Star 1') | eq(831600)

def run2(presents):
    pass

# run2(example1) | eq()

# run2(input_lines) | debug('Star 2')
