from repo_utils import *

input_lines = get_input_lines()

Timestamp = namedtuple(
    'Timestamp',
    ['year', 'month', 'day', 'hour', 'minute'],
)

def calc_sleep_time(sleep_range):
    start, end = sleep_range

    return end.minute - start.minute

def parse_logs(lines):
    guard_sleep_ranges = defaultdict(list)

    current_guard_id = None
    for line in sorted(lines):
        left, right = line[1:].lower().split('] ')

        date, time = left.split()

        year, month, day = [int(x) for x in date.split('-')]
        hour, minute = [int(x) for x in time.split(':')]
        timestamp = Timestamp(year, month, day, hour, minute)

        info = right.split()
        if info[0] == 'guard':
            current_guard_id = int(info[1][1:])
        elif info[0] == 'falls':
            guard_sleep_ranges[current_guard_id].append([timestamp])
        elif info[0] == 'wakes':
            guard_sleep_ranges[current_guard_id][-1].append(timestamp)

    return guard_sleep_ranges

def run(lines):
    guard_sleep_ranges = parse_logs(lines)

    ans = 0
    max_sleep_time = 0
    for guard_id, sleep_ranges in guard_sleep_ranges.items():
        total_sleep_time = sum(
            calc_sleep_time(sleep_range)
            for sleep_range in sleep_ranges
        )
        if total_sleep_time <= max_sleep_time:
            continue

        max_sleep_time = total_sleep_time

        minute_counter = Counter()
        for start, end in sleep_ranges:
            for minute in range(start.minute, end.minute):
                minute_counter[minute] += 1

        most_common_minute = minute_counter.most_common()[0][0]
        ans = guard_id * most_common_minute

    return ans

def run2(lines):
    guard_sleep_ranges = parse_logs(lines)

    ans = 0
    max_sleep_minutes = 0
    for guard_id, sleep_ranges in guard_sleep_ranges.items():
        minute_counter = Counter()
        for start, end in sleep_ranges:
            for minute in range(start.minute, end.minute):
                minute_counter[minute] += 1

        most_common_minute, counts = minute_counter.most_common()[0]
        if max_sleep_minutes < counts:
            ans = guard_id * most_common_minute
            max_sleep_minutes = counts

    return ans

example1 = multiline_lines(r"""
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
""")

run(example1) | eq(240)

run(input_lines) | debug('Star 1') | eq(103720)

run2(example1) | eq(4455)

run2(input_lines) | debug('Star 2') | eq(110913)
