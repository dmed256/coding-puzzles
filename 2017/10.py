from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

class Problem:
    def __init__(self, problem, lines, length):
        self.problem = problem

        self.lengths = [int(x) for x in lines[0].split(',')]

        if self.problem == 1:
            self.rounds = 1
            self.values = list(range(length))
        else:
            self.rounds = 64
            self.values = [
                ord(c)
                for c in str(range(length))[1:-1]
            ]
            self.values += [17, 31, 73, 47, 23]

    def run(self):
        values = self.values

        ptr = 0
        for _ in range(self.rounds):
            for skip, length in enumerate(self.lengths):
                if length > len(values):
                    continue

                p1 = ptr
                p2 = (ptr + length) % len(values)

                ptr = (ptr + length + skip) % len(values)

                if p1 < p2:
                    values[p1:p2] = reversed(values[p1:p2])
                elif length:
                    start = values[:p2]
                    end = values[p1:]
                    chunk = (end + start)[::-1]
                    values[:p2] = chunk[len(end):]
                    values[p1:] = chunk[:len(end)]

        if self.problem == 1:
            return values[0] * values[1]

        hash_value = []
        for i in range(0, len(values), 16):
            h = 0
            for v in values[i:i + 16]:
                h ^= v
            hash_value.append(chr(h))

        print(hash_value)

def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

example1 = multiline_lines(r"""
3, 4, 1, 5
""")

run(example1, 5) | eq(12)

run(input_lines, 256) | debug('Star 1') | eq(8536)

# run2(example1, 5) | eq()

# run2(input_lines) | debug('Star 2') | clipboard()
