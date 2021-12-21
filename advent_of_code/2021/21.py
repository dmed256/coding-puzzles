from repo_utils import *

def run1(p1, p2):
    p1 -= 1
    p2 -= 1

    dice = 1
    p1_score = 0
    p2_score = 0
    while True:
        move = (3 * dice) + 3
        p1 = (p1 + move) % 10
        p1_score += p1 + 1
        dice += 3
        if p1_score >= 1000:
            break

        move = (3 * dice) + 3
        p2 = (p2 + move) % 10
        p2_score += p2 + 1
        dice += 3
        if p2_score >= 1000:
            break

    return min([p1_score, p2_score]) * (dice - 1)

@functools.cache
def roll(p1, p2, player_turn, rolls_left, roll_amt, p1_score, p2_score):
    w1 = 0
    w2 = 0
    if rolls_left:
        for d in range(1, 4):
            w1_, w2_ = roll(
                p1,
                p2,
                player_turn,
                rolls_left - 1,
                roll_amt + d,
                p1_score,
                p2_score,
            )
            w1 += w1_
            w2 += w2_
        return w1, w2

    if player_turn == 0:
        p1 = (p1 + roll_amt) % 10
        p1_score += p1 + 1
        if 21 <= p1_score:
            w1 += 1
            return w1, w2
    else:
        p2 = (p2 + roll_amt) % 10
        p2_score += p2 + 1
        if 21 <= p2_score:
            w2 += 1
            return w1, w2

    w1_, w2_ = roll(
        p1,
        p2,
        (player_turn + 1) % 2,
        3,
        0,
        p1_score,
        p2_score,
    )
    w1 += w1_
    w2 += w2_
    return w1, w2

def run2(p1, p2):
    return max(roll(p1 - 1, p2 - 1, 0, 3, 0, 0, 0))

run1(4, 8) | eq(739785)

run1(2, 8) | debug('Star 1') | eq(1196172)

run2(4, 8) | eq(444356092776315)

run2(2, 8) | debug('Star 2') | eq(106768284484217)
