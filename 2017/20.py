from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

def get_vector(s):
    return [
        int(x.strip())
        for x in s[:-1].split('<')[1].split(',')
    ]

def get_magnitude(v):
    return sum(x*x for x in v)

def run(problem, lines):
    particles = []
    for line in lines:
        [p, v, a] = line.split(', ')
        particles.append((
            get_vector(p),
            get_vector(v),
            get_vector(a),
        ))

    default_indices = list(range(len(particles)))

    if problem == 1:
        def particle_sort_key(i):
            [p1, v1, a1] = [get_magnitude(v) for v in particles[i]]
            return (a1, v1, p1)

        # px(t) = p[x] + v[x]*t + 0.5 * a[x] * t^2
        return sorted(
            default_indices,
            key=particle_sort_key
        )[0]

    def particle_magnitude_sort_key(axis):
        def sort_key(i):
            p, v, a = particles[i]
            return (a[axis], v[axis], p[axis])
        return sort_key

    def particle_position_sort_key(axis):
        def sort_key(i):
            p, v, a = particles[i]
            return p[axis]
        return sort_key

    end_states = [
        sorted(default_indices, key=particle_magnitude_sort_key(axis))
        for axis in range(3)
    ]

    alive_indices = default_indices

    while True:
        positions = {}
        for i in alive_indices:
            p, v, a = particles[i]
            v = [v[i] + a[i] for i in range(3)]
            p = [p[i] + v[i] for i in range(3)]
            particles[i] = (p, v, a)

            pos = tuple(p)
            if pos not in positions:
                positions[pos] = []
            positions[pos].append(i)

        intersections = {
            index
            for indices in positions.values()
            if len(indices) > 1
            for index in indices
        }
        if intersections:
            alive_indices = [x for x in alive_indices if x not in intersections]
            end_states = [
                [x for x in axis_end_state if x not in intersections]
                for axis_end_state in end_states
            ]

        position_states = [
            sorted(alive_indices, key=particle_position_sort_key(axis))
            for axis in range(3)
        ]
        if position_states == end_states:
            break

    return len(alive_indices)

example1 = multiline_lines(r"""
p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>
""")

run(1, example1) | eq(0)

run(1, input_lines) | debug('Star 1') | eq(457)

example2 = multiline_lines(r"""
p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>
""")

run(2, example2) | eq(1)

run(2, input_lines) | debug('Star 2') | eq(448)
