from repo_utils import *

input_lines = get_input_lines()

def play_game(problem, p1, p2):
    cache = set()
    while p1 and p2:
        winner = None
        if problem == 2:
            key = (tuple(p1), tuple(p2))
            if key in cache:
                winner = 1
            cache.add(key)

        c1 = p1.pop(0)
        c2 = p2.pop(0)

        needs_subgame = (
            problem == 2
            and winner is None
            and len(p1) >= c1
            and len(p2) >= c2
        )
        if needs_subgame:
            sub_p1 = p1[:c1]
            sub_p2 = p2[:c2]
            # This specific optimization is taken from subreddit wisdom
            # I couldn't figure out the trick to speed this up :(
            #
            # max(sub_p1) > max(sub_p2)
            # -> If there are no recusive games, P1 will always win
            #    due to having the largest card
            #
            # max(sub_p1) > c1 + c2 - 2
            # -> This won't cause any recursive games due to
            #    len(p#) < max(sub_p1)
            #
            # This doesn't apply to P2 because repeats cause P1 to win
            if max(sub_p1) > max(sub_p2) and max(sub_p1) > c1 + c2 - 2:
                winner = 1
            else:
                winner, _ = play_game(problem, sub_p1, sub_p2)

        if winner is None:
            winner = 1 if c1 > c2 else 2

        if winner == 1:
            p1 += [c1, c2]
        else:
            p2 += [c2, c1]

    if p1:
        winner = (1, p1)
    else:
        winner = (2, p2)

    return winner


def run(problem, lines):
    players = []
    for line in lines:
        if not line:
            continue
        if line.startswith('Player'):
            players.append([])
        else:
            players[-1].append(int(line))

    _, deck = play_game(
        problem,
        players[0],
        players[1],
    )

    return sum(
        (i + 1) * c
        for i, c in enumerate(reversed(deck))
    )

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

run(1, example1) | eq(306)

run(1, input_lines) | debug('Star 1') | eq(29764)

run(2, example1) | eq(291)

run(2, input_lines) | debug('Star 2') | eq(32588)
