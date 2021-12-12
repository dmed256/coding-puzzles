from repo_utils import *

input_value = get_input()
input_lines = get_input_lines()

def run(lines, problem):
    recipes = {}
    field_names = []
    for line in lines:
        [name, info] = line.split(': ')
        recipes[name] = {
            words[0]: int(words[1])
            for fields in info.split(', ')
            if (words := fields.split(' '))
        }
        field_names = list(recipes[name].keys())

    def get_score(amounts):
        score = 1
        for field in field_names:
            if field == 'calories':
                continue
            field_score = 0
            for amount, recipe in zip(amounts, recipes.values()):
                field_score += amount * recipe[field]
            if field_score < 0:
                return 0
            score *= field_score
        return score

    def split_amounts(amount, count):
        if count == 1:
            return [[amount]]

        amounts = []
        for i in range(amount):
            for others in split_amounts(amount - i, count - 1):
                amounts.append([i, *others])
        return amounts

    def get_calories(amounts):
        return sum(
            amount * recipe['calories']
            for amount, recipe in zip(amounts, recipes.values())
        )

    recipe_count = len(recipes)
    amounts = split_amounts(100, recipe_count)
    if problem == 2:
        amounts = [
            amount
            for amount in amounts
            if get_calories(amount) == 500
        ]

    return max(
        get_score(amounts)
        for amounts in amounts
    )

example1 = multiline_lines(r"""
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
""")

run(example1, 1) | eq(62842880)
run(input_lines, 1) | debug('Star 1') | eq(13882464)

run(example1, 2) | eq(57600000)
run(input_lines, 2) | debug('Star 2') | eq(11171160)
