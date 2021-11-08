import math
from advent_of_code import *

def get_recipes(lines):
    recipes = {}
    for line in lines:
        [inputs, output] = line.split(' => ')
        inputs = [
            x.strip().split(' ')
            for x in inputs.split(',')
        ]
        inputs = [
            [int(amount), material]
            for [amount, material] in inputs
        ]

        [amount_produced, material] = output.split(' ')

        recipes[material] = [int(amount_produced), inputs]

    return recipes

def get_dependencies(recipes):
    # Find dependencies
    dependencies = {
        material: set([
            dependency_material
            for [_, dependency_material] in recipes[material][1]
        ])
        for material in recipes.keys()
    }
    dependencies['ORE'] = set()

    while True:
        applied_updates = False
        for material, deps in dependencies.items():
            dep_updates = set()
            for dep in deps:
                dep_updates.update(dependencies[dep] - deps)
            if dep_updates:
                dependencies[material].update(dep_updates)
                applied_updates = True

        if not applied_updates:
            break

    return dependencies

def find_ore_cost(recipes, dependencies, fuel):
    requirements = { 'FUEL': fuel, 'ORE': 0 }
    while requirements:
        next_requirements = requirements.copy()

        required_materials = set(requirements.keys())
        required_dependencies = set()
        for material in required_materials:
            required_dependencies.update(dependencies[material])

        convertable_materials = [
            material
            for material in required_materials
            if material not in required_dependencies
            and material != 'ORE'
        ]

        for material in convertable_materials:
            amount_required = requirements[material]
            [amount_produced, inputs] = recipes[material]

            recipes_needed = math.ceil(amount_required / amount_produced)

            for [amount, dep_material] in inputs:
                amount_needed = recipes_needed * amount

                current_amount_required = next_requirements.get(dep_material, 0)
                next_requirements[dep_material] = (
                    current_amount_required
                    + (recipes_needed * amount)
                )

            del next_requirements[material]

        if requirements == next_requirements:
            break

        requirements = next_requirements

    return requirements['ORE']

def run(lines):
    recipes = get_recipes(lines)
    dependencies = get_dependencies(recipes)
    return find_ore_cost(recipes, dependencies, 1)

example1 = multiline_lines("""
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
""")

example2 = multiline_lines("""
9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL
""")

example3 = multiline_lines("""
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
""")

example4 = multiline_lines("""
2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF
""")

example5 = multiline_lines("""
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
""")

run(example1) | eq(31)
run(example2) | eq(165)
run(example3) | eq(13312)
run(example4) | eq(180697)
run(example5) | eq(2210736)

input_lines = get_input_lines()

run(input_lines) | debug('Star 1') | eq(362713)

A_TRILLION = 1000000000000

def run2(lines):
    recipes = get_recipes(lines)
    dependencies = get_dependencies(recipes)

    start = 0
    end = A_TRILLION
    pivot = (end + start) // 2
    while start < pivot < end:
        ore_cost = find_ore_cost(recipes, dependencies, pivot)
        if ore_cost < A_TRILLION:
            start = pivot
            pivot = (end + pivot) // 2
        elif ore_cost > A_TRILLION:
            end = pivot
            pivot = (start + pivot) // 2
        else:
            start = end = pivot

    return pivot

run2(example3) | eq(82892753)
run2(example4) | eq(5586022)
run2(example5) | eq(460664)

run2(input_lines) | debug('Star 2') | eq(3281820)
