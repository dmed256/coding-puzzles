from repo_utils import *

input_value = get_input()
input_lines = get_input_lines()

class Problem:
    def __init__(self, problem, lines):
        self.problem = problem

        towers = {}
        for line in lines:
            if '->' in line:
                [left, right] = line.split(' -> ')
            else:
                [left, right] = [line, None]

            [tower, weight] = left[:-1].split(' (')
            weight = int(weight)

            if right:
                deps = right.split(', ')
            else:
                deps = []

            towers[tower] = (weight, deps)

        self.towers = towers

    def traverse_towers(self, tower, depth, cache):
        if tower in cache:
            return cache[tower]

        weight, deps = self.towers[tower]
        weight += sum(
            self.traverse_towers(dep, depth + 1, cache)
            for dep in deps
        )

        cache[tower] = (weight, depth)
        return weight

    def run(self):
        towers = self.towers

        is_dep = set()
        for tower, (weight, deps) in towers.items():
            is_dep |= set(deps)

        root_tower = list(
            set(towers.keys()) - is_dep
        )[0]

        if self.problem == 1:
            return root_tower

        tower_info = {}
        self.traverse_towers(root_tower, 0, tower_info)

        tower_weights = {
            tower: info[0]
            for tower, info in tower_info.items()
        }
        tower_depths = {
            tower: info[1]
            for tower, info in tower_info.items()
        }

        max_depth = 0
        bad_tower = root_tower
        for tower, (_, deps) in self.towers.items():
            depth = tower_depths[tower]
            weights = {
                tower_weights[dep]
                for dep in deps
            }
            if len(weights) > 1 and max_depth < depth:
                bad_tower = tower
                max_depth = depth

        _, bad_deps = self.towers[bad_tower]
        weight_counts = set()
        for dep in bad_deps:
            w = tower_weights[dep]
            if w in weight_counts:
                expected_weight = w
                break
            else:
                weight_counts.add(w)

        for dep in bad_deps:
            tower_weight, _ = towers[dep]
            total_weight = tower_weights[dep]
            if total_weight != expected_weight:
                return tower_weight + expected_weight - total_weight

def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

example1 = multiline_lines(r"""
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
""")

run(example1) | eq('tknk')

run(input_lines) | debug('Star 1') | eq('dgoocsw')

run2(example1) | eq(60)

run2(input_lines) | debug('Star 2') | eq(1275)
