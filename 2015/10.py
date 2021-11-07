from advent_of_code import *

def run(value):
    values = [int(v) for v in value]
    output = ''

    prev_c = None
    count = 0
    for c in values:
        if prev_c == c:
            count += 1
            continue

        if prev_c is not None:
            output += f'{count}{prev_c}'
        prev_c = c
        count = 1

    output += f'{count}{prev_c}'
    return output

run('1') | eq('11')
run('11') | eq('21')
run('21') | eq('1211')
run('1211') | eq('111221')
run('111221') | eq('312211')

value = '3113322113'
for i in range(40):
    value = run(value)
len(value) | debug('Star 1')


for i in range(10):
    value = run(value)
len(value) | debug('Star 2')
