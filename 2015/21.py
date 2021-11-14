import math
from advent_of_code import *

# (cost, damage, armor)
weapons = [
    (8, 4, 0),
    (10, 5, 0),
    (25, 6, 0),
    (40, 7, 0),
    (74, 8, 0),
]
armors = [
    (0, 0, 0),
    (13, 0, 1),
    (31, 0, 2),
    (53, 0, 3),
    (75, 0, 4),
    (102, 0, 5),
]
rings = [
    (25, 1, 0),
    (50, 2, 0),
    (100, 3, 0),
    (20, 0, 1),
    (40, 0, 2),
    (80, 0, 3),
]

def run():
    hit_points = 100

    boss_hit_points = 104
    boss_damage = 8
    boss_armor = 1

    def wins(attack, defense):
        b_attack = max(1, boss_damage - defense)
        b_turns = (hit_points // b_attack) + bool(hit_points % b_attack)

        my_attack = max(1, attack - boss_armor)
        my_turns = (boss_hit_points // my_attack) + bool(boss_hit_points % my_attack)

        return my_turns <= b_turns

    min_money = 100000000
    for (cost, attack, _) in weapons:
        if cost >= min_money:
            continue
        for (acost, _, defense) in armors:
            cost2 = cost + acost
            if cost2 >= min_money:
                continue
            if wins(attack, defense):
                min_money = cost2
            for ri in range(1, 3):
                for bought_rings in itertools.combinations(rings, ri):
                    cost3 = cost2 + sum(r[0] for r in bought_rings)
                    if cost3 >= min_money:
                        continue
                    rattack = attack + sum(r[1] for r in bought_rings)
                    rdefense = defense + sum(r[2] for r in bought_rings)
                    if wins(rattack, rdefense):
                        min_money = cost3

    return min_money

run() | debug('Star 1')

def run2():
    hit_points = 100

    boss_hit_points = 104
    boss_damage = 8
    boss_armor = 1

    def wins(attack, defense):
        b_attack = max(1, boss_damage - defense)
        b_turns = (hit_points // b_attack) + bool(hit_points % b_attack)

        my_attack = max(1, attack - boss_armor)
        my_turns = (boss_hit_points // my_attack) + bool(boss_hit_points % my_attack)

        return my_turns <= b_turns

    max_money = 0
    for (cost, attack, _) in weapons:
        for (acost, _, defense) in armors:
            cost2 = cost + acost
            if cost2 >= max_money and not wins(attack, defense):
                max_money = cost2
            for ri in range(1, 3):
                for bought_rings in itertools.combinations(rings, ri):
                    cost3 = cost2 + sum(r[0] for r in bought_rings)
                    if cost3 <= max_money:
                        continue
                    rattack = attack + sum(r[1] for r in bought_rings)
                    rdefense = defense + sum(r[2] for r in bought_rings)
                    if not wins(rattack, rdefense):
                        max_money = cost3

    return max_money

run2() | debug('Star 2')
