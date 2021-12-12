from repo_utils import *

input_value = get_input()
input_lines = get_input_lines()

class Problem:
    def __init__(self, problem, lines):
        self.problem = problem
        self.grid = Grid(lines)

        x = lines[0].index('|')
        self.pos = (x, 0)
        self.direction = GRID_DOWN

    def run(self):
        visited_positions = set([self.pos])
        letters = ''
        steps = 0
        while True:
            self.pos = self.grid.apply_direction(self.pos, self.direction)
            steps += 1

            value = self.grid[self.pos]
            visited_positions.add(self.pos)

            if value == ' ':
                break

            if value.isalpha():
                letters += value
                continue

            if value != '+':
                continue

            next_pos = [
                pos
                for pos in self.grid.neighbors(self.pos)
                if self.grid[pos] != ' '
                and pos not in visited_positions
            ][0]

            self.direction = (next_pos[0] - self.pos[0], next_pos[1] - self.pos[1])

        return letters if self.problem == 1 else steps

def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

example1 = multiline_lines(r"""
     |
     |  +--+
     A  |  C
 F---|----E|--+
     |  |  |  D
     +B-+  +--+
""")

run(example1) | eq('ABCDEF')

run(input_lines) | debug('Star 1') | eq('UICRNSDOK')

run2(example1) | eq(38)

run2(input_lines) | debug('Star 2') | eq(16064)
