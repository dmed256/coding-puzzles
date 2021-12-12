from advent_of_code import *

def run(problem, floors):
    all_items = [
        item
        for floor in floors
        for item in floor
    ]
    item_indices = {
        item: i
        for i, item in enumerate(all_items)
    }
    item_count = len(all_items)
    all_items_mask = (1 << item_count) - 1

    len_items = {
        v: bit_count(v)
        for v in range(all_items_mask + 1)
    }

    def get_item_types(items, find_item_type):
        return {
            material
            for material, item_type in items
            if item_type == find_item_type
        }

    def is_valid(items):
        generator_types = get_item_types(items, 'generator')
        microchip_types = get_item_types(items, 'microchip')

        if len(generator_types) == 0:
            return True

        return microchip_types <= generator_types

    def get_items_key(items):
        key = 0
        for item in items:
            key += 1 << item_indices[item]
        return key

    valid_combinations = {
        get_items_key(items)
        for items in get_subgroups(all_items)
        if is_valid(items)
    }

    floors = [
        get_items_key(items)
        for items in floors
    ]

    queue = [(0, floors, 0)]
    cache = set()
    max_step = 0
    while queue:
        pos, floors, steps = queue.pop(0)
        max_step = max(max_step, steps)

        key = (pos, tuple(floors))
        if key in cache:
            continue
        cache.add(key)

        if floors[3] == all_items_mask:
            return steps

        floor_items = floors[pos]
        items_taken_combinations = [
            items
            for items in valid_combinations
            if 1 <= len_items[items] <= 2
            and items & floor_items == items
        ]
        for floor in range(4):
            # We need to move
            if pos == floor:
                continue

            for items_taken in items_taken_combinations:
                new_floor_items = floors[floor] + items_taken
                if new_floor_items in valid_combinations:
                    new_floors = [v for v in floors]
                    new_floors[floor] = new_floor_items
                    new_floors[pos] = floors[pos] - floor_items

                    queue.append((floor, new_floors, steps + 1))

    print(max_step)

example_floors = [
    [('hydrogen', 'microchip'), ('lithium', 'microchip')],
    [('hydrogen', 'generator')],
    [('lithium', 'generator')],
    [],
]

input_floors = [
    [('promethium', 'generator'), ('promethium', 'microchip')],
    [('cobalt', 'generator'), ('curium', 'generator'), ('ruthenium', 'generator'), ('plutonium', 'generator')],
    [('cobalt', 'microchip'), ('curium', 'microchip'), ('ruthenium', 'microchip'), ('plutonium', 'microchip')],
    [],
]

# run(1, example_floors) | eq(11)

# run(1, input_floors) | debug('Star 1') | clipboard()

# run(2, example1) | eq()

# run(2, input_lines) | debug('Star 2') | clipboard()
