import math
from advent_of_code import *

class Character:
    def __init__(self, *, hitpoints=0, gold_spent=0, attack=0, defense=0):
        self.hitpoints = hitpoints
        self.gold_spent = gold_spent
        self.attack = attack
        self.defense = defense

    def reset(self, items):
        self.hitpoints = 100
        self.gold_spent = 0
        self.attack = 0
        self.defense = 0

        for item in items:
            self.gold_spent += item.cost
            self.attack += item.attack
            self.defense += item.defense

    def can_win(self):
        global boss

        boss_dmg = max(1, boss.attack - self.defense)
        boss_ttk = math.ceil(self.hitpoints / boss_dmg)

        my_dmg = max(1, self.attack - boss.defense)
        my_ttk = math.ceil(boss.hitpoints / my_dmg)

        return my_ttk <= boss_ttk

boss = Character(
    hitpoints=104,
    attack=8,
    defense=1,
)

class Item(BaseModel):
    cost = 0
    attack = 0
    defense = 0

weapons = [
    Item(cost=8, attack=4, defense=0),
    Item(cost=10, attack=5, defense=0),
    Item(cost=25, attack=6, defense=0),
    Item(cost=40, attack=7, defense=0),
    Item(cost=74, attack=8, defense=0),
]
armors = [
    Item(cost=13, attack=0, defense=1),
    Item(cost=31, attack=0, defense=2),
    Item(cost=53, attack=0, defense=3),
    Item(cost=75, attack=0, defense=4),
    Item(cost=102, attack=0, defense=5),
]
rings = [
    Item(cost=25, attack=1, defense=0),
    Item(cost=50, attack=2, defense=0),
    Item(cost=100, attack=3, defense=0),
    Item(cost=20, attack=0, defense=1),
    Item(cost=40, attack=0, defense=2),
    Item(cost=80, attack=0, defense=3),
]

def run():
    def buy_weapon():
        for weapon in weapons:
            yield [weapon]

    def buy_armor():
        yield []
        for armor in armors:
            yield [armor]

    def buy_rings():
        yield []
        for i in range(1, 3):
            for bought_rings in itertools.combinations(rings, i):
                yield list(bought_rings)

    me = Character()
    min_amount = 10000000000
    max_amount = 0
    for bought_weapon in buy_weapon():
        for bought_armor in buy_armor():
            for bought_rings in buy_rings():
                me.reset(bought_weapon + bought_armor + bought_rings)
                if me.can_win():
                    min_amount = min(min_amount, me.gold_spent)
                else:
                    max_amount = max(max_amount, me.gold_spent)

    return (min_amount, max_amount)

(min_amount, max_amount) = run()

min_amount | debug('Star 1') | eq(78)
max_amount | debug('Star 2') | eq(148)
