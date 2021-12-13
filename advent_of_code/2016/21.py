from repo_utils import *

input_lines = get_input_lines()

def run(password, lines):
    original_lines = deepcopy(lines)
    original_password = password

    password = [c for c in password]

    based_shifts = {
        i: -((i + (1 if i < 4 else 2)) % len(password))
        for i in range(len(password))
    }

    for line in lines:
        ins, word1, *words = line.split()

        if ins == 'swap' and word1 == 'position':
            p1 = int(words[0])
            p2 = int(words[-1])
            t = password[p1]
            password[p1] = password[p2]
            password[p2] = t
        elif ins == 'swap' and word1 == 'letter':
            p1 = password.index(words[0])
            p2 = password.index(words[-1])
            t = password[p1]
            password[p1] = password[p2]
            password[p2] = t
        elif ins == 'rotate' and word1 == 'left':
            amt = int(words[0])
            password = [
                password[(i + amt) % len(password)]
                for i in range(len(password))
            ]
        elif ins == 'rotate' and word1 == 'right':
            amt = int(words[0])
            password = [
                password[(i - amt) % len(password)]
                for i in range(len(password))
            ]
        elif ins == 'rotate' and word1 == 'based':
            amt = based_shifts[
                password.index(words[-1])
            ]
            password = [
                password[(i + amt) % len(password)]
                for i in range(len(password))
            ]
        elif ins == 'reverse':
            p1 = int(words[0])
            p2 = int(words[-1]) + 1
            password[p1:p2] = list(reversed(password[p1:p2]))
        elif ins == 'move':
            p1 = int(words[0])
            p2 = int(words[-1])
            v = password.pop(p1)
            password.insert(p2, v)

    return ''.join(password)

def run2(password, lines):
    for possible in itertools.permutations(password):
        if run(possible, lines) == password:
            return ''.join(possible)

example1 = multiline_lines(r"""
swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d
""")

run('abcde', example1) | eq('decab')

run('abcdefgh', input_lines) | debug('Star 1') | eq('gfdhebac')

run2('fbgdceah', input_lines) | debug('Star 2') | eq('dhaegfbc')
