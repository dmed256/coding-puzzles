from advent_of_code import *

class Node(BaseModel):
    next_node: int

class Problem:
    def __init__(self, problem, labels, moves):
        self.problem = problem
        self.labels = [int(x) - 1 for x in labels]
        self.moves = moves

        if problem == 2:
            self.labels += list(range(len(labels), 1000000))

    def run(self):
        labels = self.labels
        count = len(labels)
        nodes = {
            labels[i]: Node(next_node=labels[(i + 1) % count])
            for i in range(count)
        }

        current = labels[0]
        for i in range(self.moves):
            n1 = nodes[current].next_node
            n2 = nodes[n1].next_node
            n3 = nodes[n2].next_node

            next_current = nodes[n3].next_node
            nodes[current].next_node = next_current

            taken = [n1, n2, n3]
            dest = (current - 1) % count
            while dest in taken:
                dest = (dest - 1) % count

            end_node = nodes[dest].next_node
            nodes[dest].next_node = n1
            nodes[n3].next_node = end_node

            current = next_current

        if self.problem == 1:
            current = 0
            output = ''
            for i in range(count - 1):
                current = nodes[current].next_node
                output += str(current + 1)
            return output

        n1 = nodes[0].next_node
        n2 = nodes[n1].next_node
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
run2(input1, 10000000) | debug('Star 2') | clipboard
