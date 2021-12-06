from advent_of_code import *

# Magic Missile costs 53 mana. It instantly does 4 damage.
# Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
# Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it is active, your armor is increased by 7.
# Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the start of each turn while it is active, it deals the boss 3 damage.
# Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the start of each turn while it is active, it gives you 101 new mana.

class State(BaseModel):
    boss_hp: int = 55
    boss_dmg: int = 8
    hp: int = 50
    mana: int = 500
    mana_spent: int = 0
    shield_turns: int = 0
    poison_turns: int = 0
    recharge_turns: int = 0

    def key(self):
        return (
            self.boss_hp,
            self.hp,
            self.mana,
            self.mana_spent,
            self.shield_turns,
            self.poison_turns,
            self.recharge_turns,
        )

    def debug_print(self):
        print(self.json())

    def apply_effects(self):
        if self.shield_turns:
            self.shield_turns -= 1

        if self.poison_turns:
            self.boss_hp -= 3
            self.poison_turns -= 1

        if self.recharge_turns:
            self.mana += 101
            self.recharge_turns -= 1

        return self

    def apply_boss_turn(self):
        self.apply_effects()

        if self.won():
            return self

        dmg = self.boss_dmg
        if self.shield_turns:
            dmg = max(1, dmg - 7)

        self.hp -= dmg

        return self

    def lost(self):
        return self.hp <= 0 or self.mana <= 0

    def won(self):
        return self.boss_hp <= 0

class Problem:
    def __init__(self, problem, init_state):
        self.problem = problem
        self.init_state = init_state

    def apply_spells(self, state):
        state.apply_effects()

        updates = []
        if state.mana > 53:
            updates.append({
                'mana': state.mana - 53,
                'mana_spent': state.mana_spent + 53,
                'boss_hp': state.boss_hp - 4,
            })
        if state.mana > 73:
            updates.append({
                'mana': state.mana - 73,
                'mana_spent': state.mana_spent + 73,
                'boss_hp': state.boss_hp - 2,
                'hp': state.hp + 2,
            })
        if state.mana > 113 and not state.shield_turns:
            updates.append({
                'mana': state.mana - 113,
                'mana_spent': state.mana_spent + 113,
                'shield_turns': 6,
            })
        if state.mana > 173 and not state.poison_turns:
            updates.append({
                'mana': state.mana - 173,
                'mana_spent': state.mana_spent + 173,
                'poison_turns': 6,
            })
        if state.mana > 229 and not state.recharge_turns:
            updates.append({
                'mana': state.mana - 229,
                'mana_spent': state.mana_spent + 229,
                'recharge_turns': 5,
            })

        valid_next_states = []
        for update in updates:
            next_state = state.copy(update=update)
            if self.problem == 2:
                next_state.hp -= 1

            if next_state.lost():
                continue

            if next_state.won():
                valid_next_states.append(next_state)
                continue

            next_state.apply_boss_turn()
            if not next_state.lost():
                valid_next_states.append(next_state)

        return valid_next_states

    @staticmethod
    def pop_min_state(states):
        idx = 0
        min_mana_spent = states[0].mana_spent
        for i in range(1, len(states)):
            if states[i].mana_spent < min_mana_spent:
                min_mana_spent = states[i].mana_spent
                idx = i

        min_state = states[idx]
        states[idx] = states[-1]
        states[-1] = min_state

        return states.pop()

    def run(self):
        states = [self.init_state]
        cache = {states[0].key()}

        min_mana = None
        while states:
            state = self.pop_min_state(states)
            if min_mana is not None and state.mana_spent >= min_mana:
                break

            if state.won():
                min_mana = safe_min(min_mana, state.mana_spent)

            for state in self.apply_spells(state):
                key = state.key()
                if key not in cache:
                    states.append(state)
                    cache.add(key)

        return min_mana

def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

run(State(
    boss_hp=13,
    boss_dmg=8,
    hp=10,
    mana=250,
)) | eq(226)

run(State(
    boss_hp=55,
    boss_dmg=8,
    hp=50,
    mana=500,
)) | debug('Star 1') | eq(953)

run2(State(
    boss_hp=55,
    boss_dmg=8,
    hp=50,
    mana=500,
)) | debug('Star 2') | eq(1289)
