from repo_utils import *

input_lines = get_input_lines()

def run(problem, lines):
    values = [int(x) for x in lines]

    groups = 3 if problem == 1 else 4
    group_weight = sum(values) // groups

    sorted_values = sorted(values, reverse=True)
    queue = [
        (1, x, x, i)
        for i, x in enumerate(sorted_values)
    ]

    min_qe = None
    min_length = len(values)
    while queue:
        length, qe, weight, max_index = heapq.heappop(queue)

        if min_length <= length:
            continue

        if weight == group_weight:
            min_qe = safe_min(min_qe, qe)
            min_length = length
            continue

        for pwi, package_weight in enumerate(sorted_values[max_index + 1:]):
            next_max_index = max_index + pwi + 1
            next_weight = weight + package_weight
            next_qe = qe * package_weight

            if next_weight <= group_weight:
                heapq.heappush(
                    queue,
                    (length + 1, next_qe, next_weight, next_max_index),
                )

    return min_qe

example1 = multiline_lines(r"""
1
2
3
4
5
7
8
9
10
11
""")

run(1, example1) | eq(99)

run(1, input_lines) | debug('Star 1') | eq(10723906903)

run(2, example1) | eq(44)

run(2, input_lines) | debug('Star 2') | eq(74850409)
