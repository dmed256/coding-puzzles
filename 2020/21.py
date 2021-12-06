from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

class Problem:
    def __init__(self, problem, lines):
        self.problem = problem

        allergen_ingredients = {}
        recipes = []
        for line in lines:
            [ingredients, allergens] = line[:-1].split(' (contains ')
            ingredients = set(ingredients.split(' '))
            allergens = set(allergens.split(', '))

            recipes.append((ingredients, allergens))

            for allergen in allergens:
                if allergen not in allergen_ingredients:
                    allergen_ingredients[allergen] = deepcopy(ingredients)
                else:
                    allergen_ingredients[allergen] &= ingredients

        ingredient_allergen = {}
        while allergen_ingredients:
            missing_allergen_ingredients = {}
            for allergen, ingredients in allergen_ingredients.items():
                ingredients -= set(ingredient_allergen.keys())
                if len(ingredients) == 1:
                    ingredient = list(ingredients)[0]
                    ingredient_allergen[ingredient] = allergen
                else:
                    missing_allergen_ingredients[allergen] = ingredients
            allergen_ingredients = missing_allergen_ingredients

        self.recipes = recipes
        self.ingredient_allergen = ingredient_allergen

    def run(self):
        ingredients_with_allergens = set(self.ingredient_allergen.keys())

        if self.problem == 1:
            count = 0
            for ingredients, _ in self.recipes:
                count += len(ingredients - ingredients_with_allergens)
            return count

        return ','.join([
            ingredient
            for [ingredient, allergen] in sorted([
                [ingredient, allergen]
                for ingredient, allergen in self.ingredient_allergen.items()
            ], key=lambda item: item[1])
        ])

def run(lines):
    return Problem(1, lines).run()

def run2(lines):
    return Problem(2, lines).run()

example1 = multiline_lines(r"""
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
""")

run(example1) | eq(5)

run(input_lines) | debug('Star 1') | eq(2569)

run2(example1) | eq('mxmxvkd,sqjhc,fvjkl')

run2(input_lines) | debug('Star 2') | eq('vmhqr,qxfzc,khpdjv,gnrpml,xrmxxvn,rfmvh,rdfr,jxh')
