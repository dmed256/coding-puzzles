from repo_utils import *

def run1(p1, p2):
    players = [p1 - 1, p2 - 1]
    scores = [0, 0]

    turn = 0
    dice = 1
    while True:
        move = (3 * dice) + 3
        players[turn] = (players[turn] + move) % 10
        scores[turn] += players[turn] + 1
        dice += 3

        if scores[turn] >= 1000:
            break

        turn = (turn + 1) % 2

    return min(scores) * (dice - 1)

@functools.cache
def roll(players, scores, turn, rolls):
    w1 = 0
    w2 = 0
    if len(rolls) < 3:
        for new_roll in range(1, 4):
            new_rolls = tuple(list(rolls) + [new_roll])
            w1_, w2_ = roll(
                players,
                scores,
                turn,
                new_rolls,
            )
            w1 += w1_
            w2 += w2_

        return w1, w2

    players = list(players)
    scores = list(scores)

    wins = [w1, w2]
    players[turn] = (players[turn] + sum(rolls)) % 10
    scores[turn] += players[turn] + 1
    if 21 <= scores[turn]:
        wins[turn] += 1
        return wins[0], wins[1]

    w1_, w2_ = roll(
        tuple(players),
        tuple(scores),
        (turn + 1) % 2,
        tuple(),
    )
    w1 += w1_
    w2 += w2_
    return w1, w2

def run2(p1, p2):
    return max(roll(
        (p1 - 1, p2 - 1),
        (0, 0),
        0,
        tuple(),
    ))

run1(4, 8) | eq(739785)

run1(2, 8) | debug('Star 1') | eq(1196172)

run2(4, 8) | eq(444356092776315)

run2(2, 8) | debug('Star 2') | eq(106768284484217)
