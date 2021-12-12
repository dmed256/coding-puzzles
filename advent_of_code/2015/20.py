import sympy
from repo_utils import *

def run(presents, problem):
    if problem == 1:
        def has_enough_presents(divisors, _):
            house_presents = 10 * sum(divisors)
            return house_presents >= presents
    else:
        def has_enough_presents(divisors, house_number):
            house_presents = 11 * sum((
                divisor
                for divisor in divisors
                if (divisor * 50) >= house_number
            ))
            return house_presents >= presents

    def get_next_prime_count(primes, house_number, divisors):
        if not primes:
            return []

        [prime, *next_primes] = primes

        possibilities = []
        for i in range(30):
            if i:
                house_number *= prime
                divisors.update({
                    divisor * prime
                    for divisor in divisors
                })

            if has_enough_presents(divisors, house_number):
                possibilities.append(house_number)
                break

            possibilities.extend(
                get_next_prime_count(
                    next_primes,
                    house_number,
                    divisors.copy(),
                )
            )

        return possibilities

    primes = get_primes(7)
    return min(get_next_prime_count(primes, 1, {1}))

run(60, 1) | eq(4)
run(70, 1) | eq(4)
run(120, 1) | eq(6)
run(36000000, 1) | debug('Star 1') | eq(831600)

run(36000000, 2) | debug('Star 2') | eq(884520)
