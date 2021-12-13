from repo_utils import *

def run(problem, salt):
    triples = []
    triple_matches = {}
    keys = []

    hash_count = 1 if problem == 1 else 2017

    ptr = 0
    while True:
        h = f'{salt}{ptr}'
        for _ in range(hash_count):
            h = md5(h)

        if triples and ptr > triples[0][0] + 1000:
            triples = [
                (c_ptr, c)
                for c_ptr, c in triples
                if ptr <= c_ptr + 1000
            ]

        dupes5 = {
            c
            for i in range(len(h))
            if (c := h[i])
            and h[i:i + 5] == (c * 5)
        }
        if dupes5:
            for c_ptr, c in triples:
                if c in dupes5 and c_ptr not in keys:
                    insort(keys, c_ptr)
                    triple_matches[c_ptr] = ptr

        for i in range(len(h)):
            c = h[i]
            if h[i:i + 3] == (c * 3):
                triples.append((ptr, c))
                break

        if len(keys) >= 64 and ptr > keys[63] + 1000:
            return keys[63]

        ptr += 1

run(1, 'abc') | eq(22728)

run(1, 'zpqevtbw') | debug('Star 1') | eq(16106)

run(2, 'abc') | eq(22551)

run(2, 'zpqevtbw') | debug('Star 2') | eq(22423)
