from repo_utils import *

input_value = get_input()

def run(value, problem):
    capcha = 0
    count = len(value)
    for i in range(count):
        v1 = value[i]
        if problem == 1:
            v2 = value[(i + 1) % count]
        else:
            v2 = value[(i + count // 2) % count]
        if v1 == v2:
            capcha += int(v1)
    return capcha


run('1122', 1) | eq(3)
run('1111', 1) | eq(4)
run('1234', 1) | eq(0)
run('91212129', 1) | eq(9)

run(input_value, 1) | debug('Star 1') | eq(1102)

run('1212', 2) | eq(6)
run('1221', 2) | eq(0)
run('123425', 2) | eq(4)
run('123123', 2) | eq(12)
run('12131415', 2) | eq(4)
run(input_value, 2) | debug('Star 2') | eq(1076)
