from advent_of_code import *

class Problem:
    def __init__(self, problem, labels, moves):
        self.problem = problem
        self.labels = [int(x) - 1 for x in labels]
        self.moves = moves

    def move(self, labels):
        count = len(labels)
        taken = labels[1:4]
        labels = labels[4:] + [labels[0]]

        current = (labels[-1] + count - 1) % count
        while current in taken:
            current = (current + count - 1) % count

        dest = labels.index(current)
        return labels[:dest+1] + taken + labels[dest+1:]

    def run(self):
        labels = self.labels
        for i in range(self.moves):
            labels = self.move(labels)

        pos1 = labels.index(0)
        labels = labels[pos1+1:] + labels[:pos1]

        return ''.join([str(x + 1) for x in labels])

def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

example1 = '389125467'
input1 = '327465189'

run(example1, 10) | eq('92658374')
run(example1, 100) | eq('67384529')
run(input1, 100) | debug('Star 1') | eq('82934675')

# run2(example1) | eq()

# run2(input_lines) | debug('Star 2') | clipboard()
