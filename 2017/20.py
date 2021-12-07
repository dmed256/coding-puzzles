from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

class Problem:
    def __init__(self, problem, lines):
        self.problem = problem

        def get_vectors(s):
            return [
                int(x.strip())
                for x in s[:-1].split('<')[1].split(',')
            ]

        self.particles = []
        for line in lines:
            [p, v, a] = line.split(', ')
            self.particles.append((
                get_vectors(p),
                get_vectors(v),
                get_vectors(a),
            ))

        # px(t) = p[x] + v[x]*t + 0.5 * a[x] * t^2
        def get_magnitude(v):
            return sum(x*x for x in v)

        def particle_sort_key(i):
            [p1, v1, a1] = [get_magnitude(v) for v in self.particles[i]]
            return (a1, v1, p1)

        self.sorted_indices = sorted(
            list(range(len(self.particles))),
            key=particle_sort_key
        )

    def run(self):
        if self.problem == 1:
            return self.sorted_indices[0]

        # Iterate by time and finish when non-collisions are in order

def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

example1 = multiline_lines(r"""
p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>
""")

run(example1) | eq(0)

run(input_lines) | debug('Star 1') | eq(457)

example2 = multiline_lines(r"""
p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>
""")

run2(example2) | eq(1)

run2(input_lines) | debug('Star 2') | clipboard()
