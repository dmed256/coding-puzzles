from repo_utils import *

input_lines = get_input_lines()

def add_counts(counts, full_counts):
    for c, count in counts.items():
        full_counts[c] += count

def expand(pair, iterations, maps, cache):
    key = (pair, iterations)
    if key in cache:
        return cache[key]

    if iterations == 0:
        if pair[0] == pair[1]:
            counts = {pair[0]: 2}
        else:
            counts = {pair[0]: 1, pair[1]: 1}
        cache[key] = counts
        return counts

    mid = maps[pair]
    p1 = pair[0] + mid
    p2 = mid + pair[1]

    # Expand both sides
    counts1 = expand(p1, iterations - 1, maps, cache)
    counts2 = expand(p2, iterations - 1, maps, cache)

    counts = defaultdict(int)
    add_counts(counts1, counts)
    add_counts(counts2, counts)

    # Remove the duplicated mid entry
    counts[mid] -= 1

    cache[key] = counts
    return counts

def run(lines, iterations):
    value = lines[0]

    maps = {}
    for line in lines[2:]:
        left, right = line.split(' -> ')
        maps[left] = right

    cache = {}
    counts = defaultdict(int)
    for i in range(len(value) - 1):
        pair = value[i:i + 2]
        if len(pair) < 2:
            counts[pair[0]] += 1
            continue

        add_counts(
            expand(pair, iterations, maps, cache),
            counts,
        )
        # Return the middle entry
        if i:
            counts[value[i - 1]] -= 1

    return max(counts.values()) - min(counts.values())

example1 = multiline_lines(r"""
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
""")

run(example1, 10) | eq(1588)

run(input_lines, 10) | debug('Star 1') | eq(2988)

run(example1, 40) | eq(2188189693529)

run(input_lines, 40) | debug('Star 2') | eq(3572761917024)
