from repo_utils import *

input_lines = get_input_lines()

def run(problem, lines):
    guard_sleep = defaultdict(int)
    max_guard_sleep = defaultdict(int)

    current_guard = None
    sleep_start = None
    sleep_end = None
    for line in sorted(lines):
        left, right = line[1:].lower().split('] ')

        day, time = left.split()
        info = right.split()

        if info[0] == 'guard':
            current_guard = int(info[1][1:])
        elif info[0] == 'falls':
            sleep_start = (day, time)
        elif info[0] == 'wakes':
            sleep_end = (day, time)

    return None

# example1 = multiline_lines(r"""
# """)

# run(1, example1) | eq()

# run(1, input_lines) | submit(1)

# run(2, example1) | eq()

# run(2, input_lines) | submit(2)
