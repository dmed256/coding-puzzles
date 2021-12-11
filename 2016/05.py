from advent_of_code import *
from hashlib import md5

def run(door):
    counter = 0
    ans1 = ''
    ans2 = [' '] * 8
    while True:
        s = f'{door}{counter}'
        h = md5(s.encode('utf-8')).hexdigest()
        if h.startswith('00000'):
            if len(ans1) < 8:
                ans1 += h[5]

            pos = int_or(h[5], -1)
            val = h[6]
            if 0 <= pos <= 7 and ans2[pos] == ' ':
                ans2[pos] = val

            if ' ' not in ans2:
                break

        counter += 1

    return ans1, ''.join(ans2)

ans1, ans2 = run('ugkcyxxp')

ans1 | debug('Star 1') | eq('d4cd2ee1')
ans2 | debug('Star 2') | eq('f2c730e5')
