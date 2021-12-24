from repo_utils import *
from utils import *

class Problem:
    def __init__(self, problem, content):
        self.problem = problem
        self.content = content

    @staticmethod
    def get_hex_bits(c):
        value = int(f'0x{c}', 0)

        h = ''
        for bit in range(4):
            h += '1' if value & (1 << bit) else '0'

        return h[::-1]

    def find_region(self, pos, missing_squares):
        group = {pos}
        queue = [pos]
        while queue:
            pos = queue.pop()
            (r, c) = pos
            for direction in DIRECTIONS:
                pos2 = apply_direction(pos, direction)
                if pos2 in missing_squares:
                    queue.append(pos2)
                    group.add(pos2)
                    missing_squares.remove(pos2)
        return group

    def run(self):
        grid = []
        for i in range(128):
            knot_hash = get_knot_hash(f'{self.content}-{i}')
            grid.append(
                ''.join([
                    self.get_hex_bits(c)
                    for c in knot_hash
                ])
            )

        squares = [
            (r, c)
            for r, row in enumerate(grid)
            for c, char in enumerate(row)
            if char == '1'
        ]

        if self.problem == 1:
            return len(squares)

        missing_squares = set(squares)
        region_count = 0
        while missing_squares:
            pos = min(missing_squares)
            missing_squares.remove(pos)

            region = self.find_region(pos, missing_squares)
            missing_squares -= region
            region_count += 1

        return region_count


def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

run('flqrgnkx') | eq(8108)
run('oundnydw') | debug('Star 1') | eq(8106)

run2('flqrgnkx') | eq(1242)
run2('oundnydw') | debug('Star 2') | eq(1164)
