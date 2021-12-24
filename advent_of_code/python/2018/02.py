from repo_utils import *

input_lines = get_input_lines()

def run(lines):
    has2 = 0
    has3 = 0
    for line in lines:
        counts = defaultdict(int)
        for c in line:
            counts[c] += 1

        has2 += any(
            1
            for v in counts.values()
            if v == 2
        )
        has3 += any(
            1
            for v in counts.values()
            if v == 3
        )

    return has2 * has3

def run2(lines):
    chars = len(lines[0])

    for i in range(len(lines)):
        w1 = lines[i]
        for j in range(i + 1, len(lines)):
            w2 = lines[j]
            similar = [
                c
                for i, c in enumerate(w1)
                if c == w2[i]
            ]
            if len(similar) == chars - 1:
                return ''.join(similar)

run(input_lines) | debug('Star 1') | eq(6696)

run2(input_lines) | debug('Star 2') | eq('bvnfawcnyoeyudzrpgslimtkj')
