from repo_utils import *

input_value = get_input()
input_lines = get_input_lines()

class Problem:
    def __init__(self, problem, lines):
        self.problem = problem

        players = []
        for line in lines:
            if not line:
                continue
            if line.startswith('Player'):
                players.append([])
            else:
                players[-1].append(int(line))

        self.p1 = players[0]
        self.p2 = players[1]

    def play_game(self, p1, p2):
        cache = set()
        while p1 and p2:
            winner = None
            if self.problem == 2:
                k = (tuple(p1), tuple(p2))
                if k in cache:
                    winner = 1
                cache.add(k)

            c1 = p1.pop(0)
            c2 = p2.pop(0)

            if winner is None and self.problem == 2:
                if len(p1) >= c1 and len(p2) >= c2:
                    winner, _ = self.play_game(p1[:c1], p2[:c2])

            if winner is None:
                winner = 1 if c1 > c2 else 2

            if winner == 1:
                p1 += [c1, c2]
            else:
                p2 += [c2, c1]

        if p1:
            return 1, p1
        else:
            return 2, p2

    def run(self):
        _, deck = self.play_game(self.p1, self.p2)
        return sum(
            (i + 1) * c
            for i, c in enumerate(deck[::-1])
        )

def run(lines):
    return Problem(1, lines).run()

def run2(lines):
    return Problem(2, lines).run()

example1 = multiline_lines(r"""
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
""")

run(example1) | eq(306)

run(input_lines) | debug('Star 1') | eq(29764)

run2(example1) | eq(291)

run2(input_lines) | debug('Star 2') | eq(32588)
