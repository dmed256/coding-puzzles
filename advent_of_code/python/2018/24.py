from repo_utils import *

input_lines = get_input_lines()

class Group(BaseModel):
    id: int
    type: str
    units: int
    initiative: int
    unit_health: int
    attack: int
    attack_type: str
    weak_to: set
    immune_to: set

    @property
    def effective_power(self):
        return self.units * self.attack

    @staticmethod
    def parse(line, group_id, group_type):
        # 7079 units each with 12296 hit points (weak to fire) with an attack that does 13 bludgeoning damage at initiative 14
        line = (
            line
            .replace('units each with ', '')
            .replace('hit points ', '')
            .replace('with an attack that does ', '')
            .replace('damage at initiative ', '')
        )

        defense_info = re.search('(\([^)]*\) )', line)
        if defense_info is not None:
            defense_info = defense_info.groups()[0]
            line = line.replace(defense_info, '')

            # Remove '^(' and ') $'
            defense_info = defense_info[1:-2]

            weak_to, immune_to = Group.parse_defense_info(defense_info)
        else:
            weak_to, immune_to = set(), set()

        units, unit_health, attack, attack_type, initiative = line.split()

        return Group(
            id=group_id,
            type=group_type,
            units=units,
            unit_health=unit_health,
            attack=attack,
            attack_type=attack_type,
            initiative=initiative,
            weak_to=weak_to,
            immune_to=immune_to,
        )

    @staticmethod
    def parse_defense_info(info):
        weak_to = set()
        immune_to = set()

        for part in info.split('; '):
            defense_type, *types = (
                part
                .replace(',', '')
                .replace(' to ', ' ')
                .split()
            )
            if defense_type == 'weak':
                weak_to |= set(types)
            elif defense_type == 'immune':
                immune_to |= set(types)
            else:
                print(f'Unknown defense type: {defense_type}')
                raise 1

        return weak_to, immune_to

    @staticmethod
    def target_selection_sort_key(group):
        return (-group.effective_power, -group.initiative)

    @staticmethod
    def attacking_sort_key(group):
        return -group.initiative

    @staticmethod
    def group_types(groups):
        return len(Counter([
            group.type
            for group in groups
        ]))

    @staticmethod
    def fight(groups):
        groups.sort(key=Group.target_selection_sort_key)

        targets = {}
        groups_targeted = set()
        for group in list(groups):
            enemies = [
                other
                for other in groups
                if other.type != group.type
                and other.id not in groups_targeted
            ]
            if not enemies:
                continue

            target, unit_damage = group.choose_target(groups, enemies)
            if target:
                targets[group.id] = (target, unit_damage)
                groups_targeted.add(target.id)

        total_units_killed = 0
        groups.sort(key=Group.attacking_sort_key)
        for group in list(groups):
            if group.units == 0:
                continue

            if group.id not in targets:
                continue

            target, unit_damage = targets[group.id]
            units_killed = (group.units * unit_damage) // target.unit_health
            target.units -= min(target.units, units_killed)

            total_units_killed += units_killed

        if not total_units_killed:
            return None

        return [
            group
            for group in groups
            if 0 < group.units
        ]

    def choose_target(self, groups, enemies):
        attack_info = []
        for enemy in enemies:
            unit_damage = self.attack
            if self.attack_type in enemy.weak_to:
                unit_damage *= 2
            if self.attack_type in enemy.immune_to:
                unit_damage = 0

            attack_info.append((
                unit_damage,
                enemy.effective_power,
                enemy.initiative,
                enemy,
            ))

        unit_damage, _, _, target = sorted(attack_info, reverse=True)[0]
        if not unit_damage:
            return None, 0

        return target, unit_damage

def simulate_battle(groups, boost=0):
    groups = deepcopy(groups)
    for group in groups:
        if group.type == 'Immune System':
            group.attack += boost

    while 1 < Group.group_types(groups):
        groups = Group.fight(groups)
        if groups is None:
            return None, None

    return groups[0].type, sum(
        group.units
        for group in groups
    )

def run(problem, lines):
    group_type = None
    groups = []
    for line in lines:
        if not line:
            continue

        if ':' in line:
            group_type = line[:-1]
            continue

        groups.append(
            Group.parse(line, len(groups), group_type)
        )

    if problem == 1:
        _, units = simulate_battle(groups)
        return units

    start = 0
    end = 10000

    min_winner = None
    while start < end:
        mid = (end + start) // 2
        winner, units = simulate_battle(groups, boost=mid)

        # Stalemate
        if winner is None:
            start += 1

        if winner == 'Immune System':
            end = mid
            min_winner = safe_min(
                min_winner,
                (mid, units)
            )
        else:
            start = mid + 1

    _, units = min_winner
    return units


example1 = multiline_lines(r"""
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
""")

run(1, example1) | eq(5216)

run(1, input_lines) | debug('Star 1') | eq(29865)

run(2, example1) | eq(51)

run(2, input_lines) | debug('Star 2') | eq(2444)
