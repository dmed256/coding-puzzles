from repo_utils import *

def run(floors):
    materials = {
        material
        for floor_items in floors
        for material, _ in floor_items
    }
    material_bitmap = {
        material: 1 << (2 * i)
        for i, material in enumerate(materials)
    }

    item_count = len([
        item
        for floor_items in floors
        for item in floor_items
    ])

    items_mask = 0
    for i in range(item_count):
        items_mask += 1 << 2*i

    # Bits: 01111000
    #   - 01 -> Has (M1, 'microchip')
    #   - 11 -> Has (M2, 'generator') + (M2, 'generator')
    #   - 10 -> Has (M3, 'generator')
    #   - 00 -> Doesn't have M4
    for i, floor_items in enumerate(floors):
        value = 0
        for material, item_type in floor_items:
            material_bit = material_bitmap[material]
            if item_type == 'microchip':
                value += material_bit
            else:
                value += material_bit << 1

        floors[i] = value

    def print_floors(pos, floors):
        for floor in [3, 2, 1, 0]:
            items = floors[floor]
            E = 'E' if floor == pos else ' '

            floor += 1
            named_items = []
            for material, bit in material_bitmap.items():
                if items & bit:
                    named_items.append(f'{material} microchip')
                elif items & (bit << 1):
                    named_items.append(f'{material} generator')

                item_type = (
                    'generator'
                    if items & (bit << 1)
                    else 'microchip'
                )

            print(f'F{floor}', E, named_items)
        print()

    def get_floors_key(pos, floors):
        return (pos, tuple(floors))

    def is_valid(items):
        generators = (items >> 1) & items_mask
        if not generators:
            return True

        microchips = items & items_mask
        return microchips & generators == microchips

    def get_next_floors(floors, pos, next_pos):
        items = [
            item
            for i in range(2 * item_count)
            if (item := floors[pos] & (1 << i))
        ]

        possibles = []
        for item_taken_count in [1, 2]:
            for items_taken in itertools.combinations(items, item_taken_count):
                items_taken = sum(items_taken)

                pos_items = floors[pos] - items_taken
                next_pos_items = floors[next_pos] + items_taken
                if not is_valid(pos_items) or not is_valid(next_pos_items):
                    continue

                next_floors = list(floors)
                next_floors[pos] = pos_items
                next_floors[next_pos] = next_pos_items

                possibles.append(next_floors)

        return possibles

    queue = [(0, floors, 0)]
    cache = set(get_floors_key(0, floors))
    while queue:
        pos, floors, stops = queue.pop(0)

        if pos == 3 and not any(floors[:-1]):
            return stops

        # if not len(cache) % 100000:
        #     print(stops, len(cache))

        next_stops = stops + 1
        for next_pos in [pos - 1, pos + 1]:
            if not (0 <= next_pos <= 3):
                continue

            for next_floors in get_next_floors(floors, pos, next_pos):
                key = get_floors_key(next_pos, next_floors)
                if key in cache:
                    continue

                if not sum(floors[:next_pos+1]) and sum(floors[:next_pos+1]):
                    continue

                queue.append((next_pos, next_floors, next_stops))
                cache.add(key)

    return None

example_floors = [
    {('hydrogen', 'microchip'), ('lithium', 'microchip')},
    {('hydrogen', 'generator')},
    {('lithium', 'generator')},
    set(),
]

input_floors = [
    {('promethium', 'generator'), ('promethium', 'microchip')},
    {('cobalt', 'generator'), ('curium', 'generator'), ('ruthenium', 'generator'), ('plutonium', 'generator')},
    {('cobalt', 'microchip'), ('curium', 'microchip'), ('ruthenium', 'microchip'), ('plutonium', 'microchip')},
    set(),
]

input_floors2 = [
    {('promethium', 'generator'), ('promethium', 'microchip'), ('elerium', 'generator'), ('elerium', 'microchip'), ('dilithium', 'generator'), ('dilithium', 'microchip')},
    {('cobalt', 'generator'), ('curium', 'generator'), ('ruthenium', 'generator'), ('plutonium', 'generator')},
    {('cobalt', 'microchip'), ('curium', 'microchip'), ('ruthenium', 'microchip'), ('plutonium', 'microchip')},
    set(),
]

run(example_floors) | eq(11)

run(input_floors) | debug('Star 1') | eq(33)

run(input_floors2) | debug('Star 2') | eq(57)
