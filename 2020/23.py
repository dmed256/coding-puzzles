from advent_of_code import *

class Problem:
    def __init__(self, problem, labels, moves):
        self.problem = problem
        self.moves = moves

        labels = [int(x) - 1 for x in labels]
        count = len(labels)

        label_pointers = deepcopy(labels)
        for i in range(count):
            label_pointers[labels[i]] = labels[(i + 1) % count]

        self.start = labels[0]

        if problem == 1:
            self.pointers = label_pointers
        else:
            count = 1000000
            self.pointers = [
                (i + 1) % count
                for i in range(count)
            ]
            self.pointers[:len(labels)] = label_pointers
            self.pointers[labels[-1]] = len(labels)
            self.pointers[-1] = labels[0]

    def run(self):
        pointers = self.pointers
        current = self.start

        count = len(pointers)
        for i in range(self.moves):
            n1 = pointers[current]
            n2 = pointers[n1]
            n3 = pointers[n2]

            next_current = pointers[n3]
            pointers[current] = next_current

            taken = [n1, n2, n3]
            dest = (current - 1) % count
            while dest in taken:
                dest = (dest - 1) % count

            end_node = pointers[dest]
            pointers[dest] = n1
            pointers[n3] = end_node

            current = next_current

        if self.problem == 1:
            current = 0
            output = ''
            for i in range(count - 1):
                current = pointers[current]
                output += str(current + 1)
            return output

        n1 = pointers[0]
        n2 = pointers[n1]
        return (n1 + 1) * (n2 + 1)

def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

example1 = '389125467'
input1 = '327465189'

run(example1, 10) | eq('92658374')
run(example1, 100) | eq('67384529')
run(input1, 100) | debug('Star 1') | eq('82934675')

run2(example1, 10000000) | eq(149245887792)
run2(input1, 10000000) | debug('Star 2') | eq(474600314018)
