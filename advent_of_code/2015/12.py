from repo_utils import *

input_value = get_input()

class Problem:
    def __init__(self, problem, value):
        self.problem = problem
        self.obj = json.loads(value)

    def count(self, obj):
        if type(obj) is dict:
            if self.problem == 2:
                if 'red' in obj.values():
                    return 0
            return sum(self.count(v) for v in obj.values())
        if type(obj) is list:
            return sum(self.count(v) for v in obj)
        if type(obj) is int:
            return obj
        return 0

    def run(self):
        return self.count(self.obj)

def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

run('[1,2,3]') | eq(6)
run('{"a":2,"b":4}') | eq(6)
run('[[[3]]]') | eq(3)
run('{"a":{"b":4},"c":-1}') | eq(3)
run('{"a":[-1,1]}') | eq(0)
run('[-1,{"a":1}]') | eq(0)
run('[]') | eq(0)
run('{}') | eq(0)

run(input_value) | debug('Star 1') | eq(191164)

run2(input_value) | debug('Star 2') | eq(87842)
