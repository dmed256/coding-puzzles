from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

class Problem:
    def __init__(self, problem, lines):
        self.problem = problem

        programs = {}
        for line in lines:
            [program, values] = line.split(' <-> ')
            program = int(program)
            values = [int(x) for x in values.split(',')]
            programs[program] = values

        self.programs = programs

    def find_group(self, value):
        queue = [value]
        items = set([value])
        while queue:
            value = queue.pop()
            new_deps = set(self.programs[value]) - items
            queue += list(new_deps)
            items |= new_deps

        return items

    def run(self):
        programs = self.programs
        program_values = set(programs.keys())

        if self.problem == 1:
            return len(self.find_group(0))

        group_count = 0
        while program_values:
            value = min(program_values)
            group = self.find_group(value)
            program_values -= group
            group_count += 1

        return group_count

def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

example1 = multiline_lines(r"""
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5
""")

run(example1) | eq(6)

run(input_lines) | debug('Star 1') | eq(239)

run2(example1) | eq(2)

run2(input_lines) | debug('Star 2') | clipboard()
