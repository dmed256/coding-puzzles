from repo_utils import *

def run(values, find_turn):
    values = split_comma_ints(values)
    memory = {}
    for turn, value in enumerate(values[:-1]):
        memory[value] = turn + 1

    value = values[-1]
    turn = len(values)
    for turn in range(len(values), find_turn):
        last_turn = memory.get(value)
        if last_turn is None:
            next_value = 0
        else:
            next_value = turn - last_turn

        memory[value] = turn
        value = next_value

    return value

# run('0,3,6', 2020) | eq(436)
# run('1,3,2', 2020) | eq(1)
# run('2,1,3', 2020) | eq(10)
# run('1,2,3', 2020) | eq(27)
# run('2,3,1', 2020) | eq(78)
# run('3,2,1', 2020) | eq(438)
# run('3,1,2', 2020) | eq(1836)
run('0,8,15,2,12,1,4', 2020) | debug('Star 1') | eq(289)

# run('0,3,6', 30000000) | eq(175594)
# run('1,3,2', 30000000) | eq(2578)
# run('2,1,3', 30000000) | eq(3544142)
# run('1,2,3', 30000000) | eq(261214)
# run('2,3,1', 30000000) | eq(6895259)
# run('3,2,1', 30000000) | eq(18)
# run('3,1,2', 30000000) | eq(362)
run('0,8,15,2,12,1,4', 30000000) | debug('Star 2') | eq(1505722)
