from repo_utils import *

input_lines = get_input_lines()

def run(problem, lines):
    intervals = []
    for line in lines:
        l, r = line.split('-')
        l = int(l)
        r = int(r)
        intervals.append((l, r))

    intervals.sort()

    if problem == 1:
        ip = 0
        for left, right in intervals:
            if ip < left:
                return ip
            ip = max(ip, right + 1)

    ip = 0
    valid_ips = 0
    for left, right in intervals:
        if ip < left:
            valid_ips += left - ip
        ip = max(ip, right + 1)

    if ip < 4294967295:
        valid_ips += 4294967295 - ip

    return valid_ips

example1 = multiline_lines(r"""
5-8
0-2
4-7
""")

run(1, example1) | eq(3)

run(1, input_lines) | debug('Star 1') | eq(22887907)

run(2, input_lines) | debug('Star 2') | eq(109)
