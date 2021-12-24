from repo_utils import *

input_value = get_input()
input_lines = get_input_lines()

def has_abba(word):
    for i in range(4, len(word) + 1):
        w = word[i- 4:i]
        if w[0] == w[1]:
            continue

        if w[:2] == w[:1:-1]:
            return True

    return False

def find_aba(word):
    abas = []
    for i in range(3, len(word) + 1):
        w = word[i- 3:i]
        if w[0] == w[1]:
            continue

        if w[0] == w[2]:
            abas.append(w)

    return abas

def run(problem, lines):
    tls = 0
    ssl = 0
    for line in lines:
        words = re.split('[\[\]]', line)

        # Problem 1
        matches = [
            (word, i % 2)
            for i, word in enumerate(words)
            if has_abba(word)
        ]
        if matches:
            is_valid = all(
                not in_bracket
                for word, in_bracket in matches
            )
            tls += is_valid

        # Problem 2
        plain    = [words[i] for i in range(0, len(words), 2)]
        brackets = [words[i] for i in range(1, len(words), 2)]
        plain_aba = {
            aba
            for word in plain
            for aba in find_aba(word)
        }
        brackets_aba = {
            f'{aba[1]}{aba[0]}{aba[1]}'
            for word in brackets
            for aba in find_aba(word)
        }

        ssl += len(plain_aba & brackets_aba) > 0

    return tls if problem == 1 else ssl

example1 = multiline_lines(r"""
abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn
""")

run(1, example1) | eq(2)

run(1, input_lines) | debug('Star 1') | eq(105)

example2 = multiline_lines(r"""
aba[bab]xyz
xyx[xyx]xyx
aaa[kek]eke
zazbz[bzb]cdb
""")

run(2, example2) | eq(3)

run(2, input_lines) | debug('Star 2') | eq(258)
