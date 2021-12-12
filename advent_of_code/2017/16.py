from repo_utils import *

input_value = get_input()

class Problem:
    def __init__(self, problem, line, length):
        self.problem = problem

        self.length = length
        self.instructions = []
        for dance in line.split(','):
            ins = dance[0]
            inputs = dance[1:]
            if ins == 's':
                self.instructions.append([ins, int(inputs)])
            if ins == 'x':
                [a, b] = inputs.split('/')
                self.instructions.append([ins, int(a), int(b)])
            if ins == 'p':
                [a, b] = inputs.split('/')
                self.instructions.append([ins, a, b])

    def dance(self, word):
        for instruction in self.instructions:
            [ins, *inputs] = instruction
            if ins == 's':
                offset = inputs[0]
                word = word[-offset:] + word[:-offset]
            elif ins == 'x':
                [ai, bi] = inputs
                a = word[ai]
                word[ai] = word[bi]
                word[bi] = a
            elif ins == 'p':
                [a, b] = inputs
                ai = word.index(a)
                bi = word.index(b)
                word[ai] = b
                word[bi] = a
        return word

    def run(self):
        word = [
            chr(ord('a') + i)
            for i in range(self.length)
        ]

        if self.problem == 1:
            return ''.join(self.dance(word))

        loops = 1000000000

        order = [tuple(word)]
        cache = set(order)
        for i in range(loops):
            word = self.dance(list(word))
            key = tuple(word)
            if key in cache:
                break
            cache.add(key)
            order.append(key)

        idx = order.index(key)

        # Remove the non-cycle part
        loops -= idx
        word_cycle = order[idx:]

        return ''.join(word_cycle[loops % len(order)])

def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

run('s1', 5) | eq('eabcd')
run('s1,x3/4', 5) | eq('eabdc')
run('s1,x3/4,pe/b', 5) | eq('baedc')

run(input_value, 16) | debug('Star 1') | eq('jcobhadfnmpkglie')

run2(input_value, 16) | debug('Star 2') | eq('pclhmengojfdkaib')
