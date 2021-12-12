from repo_utils import *

input_value = get_input()
input_lines = get_input_lines()

def get_reindeer_info(lines):
    return [
        extract_ints(line)
        for line in lines
    ]

def run(lines, time):
    distance = 0
    for [speed, run_time, rest_time] in get_reindeer_info(lines):
        cycle_time = (run_time + rest_time)
        cycles = time // cycle_time

        leftover = time - (cycles * cycle_time)
        extra_run = min(leftover, run_time)

        reindeer_value = speed * (extra_run + (cycles * run_time))

        distance = max(distance, reindeer_value)

    return distance

example1 = multiline_lines(r"""
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
""")

run(example1, 1) | eq(16)
run(example1, 1000) | eq(1120)
run(input_lines, 2503) | debug('Star 1') | eq(2660)

def run2(lines, time):
    reindeer_info = get_reindeer_info(lines)

    distances = [0] * len(reindeer_info)
    scores = [0] * len(reindeer_info)
    for t in range(time):
        for i, [speed, run_time, rest_time] in enumerate(reindeer_info):
            cycle_time = (run_time + rest_time)
            tr = t % cycle_time

            if tr < run_time:
                distances[i] += speed

        max_distance = max(distances)
        for i in range(len(scores)):
            if distances[i] == max_distance:
                scores[i] += 1

    return max(scores)

run2(example1, 1000) | eq(689)
run2(input_lines, 2503) | debug('Star 2') | eq(1256)
