from repo_utils import *

input_lines = get_input_lines()

def play_game(problem, p1, p2, game_cache):
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

        if (winner is None
            and problem == 2
            and len(p1) >= c1
            and len(p2) >= c2):
            winner, _ = play_game(
                problem,
                p1[:c1],
                p2[:c2],
                game_cache,
            )

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

    game_key2 = (game_key[1], game_key[0])
    winner2 = (1 + (winner[0] % 2), winner[1])

    game_cache[game_key] = winner
    game_cache[game_key2] = winner2

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

    _, deck = play_game(problem, players[0], players[1], {})

    return sum(
        (i + 1) * c
        for i, c in enumerate(deck[::-1])
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
