from advent_of_code import *

class Problem:
    def __init__(self, problem, gen_a, gen_b):
        self.problem = problem
        self.gen_a = gen_a
        self.gen_b = gen_b

    def run2(self):
        gen_a = self.gen_a
        gen_b = self.gen_b

        a_values = []
        a_seen_values = set()

        b_values = []
        b_seen_values = set()

        for i in range(16807):
            gen_a = (gen_a * 16807) % 2147483647
            if gen_a in a_seen_values:
                break
            a_values.append(gen_a)
            a_seen_values.add(gen_a)

        for i in range(48271):
            gen_b = (gen_b * 48271) % 2147483647
            if gen_b in b_seen_values:
                break
            b_values.append(gen_b)
            b_seen_values.add(gen_b)

        len(a_values)
        len(a_values)

        mask = (1 << 16) - 1
        a_values = [v & mask for v in a_values]
        b_values = [v & mask for v in b_values]

        return len([
            1
            for i in range(40_000_000)
            if a_values[i % len(a_values)] == b_values[i % len(b_values)]
        ])

    def run(self):
        gen_a = self.gen_a
        gen_b = self.gen_b

        pairs = 40_000_000 if self.problem == 1 else 5_000_000

        count = 0
        mask = (1 << 16) - 1
        for i in range(pairs):
            gen_a = (gen_a * 16807) % 2147483647
            gen_b = (gen_b * 48271) % 2147483647

            if self.problem == 2:
                while gen_a % 4:
                    gen_a = (gen_a * 16807) % 2147483647

                while gen_b % 8:
                    gen_b = (gen_b * 48271) % 2147483647

            count += (mask & gen_a) == (mask & gen_b)

        return count


def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

run(65, 8921) | eq(588)

run(277, 349) | debug('Star 1') | eq(592)

run2(65, 8921) | eq(309)

run2(277, 349) | debug('Star 2') | clipboard()