from repo_utils import *

MICROCHIP = 1
GENERATOR = 2


def get_microchip_materials(items):
    return {
        material
        for material, item_type in items
        if item_type == MICROCHIP
    }


def get_generator_materials(items):
    return {
        material
        for material, item_type in items
        if item_type == GENERATOR
    }


def get_next_floors(floors, pos, next_pos):
    items = floors[pos]

    possible_next_floors = []
    for item_taken_count in [1, 2]:
        for items_taken in itertools.combinations(items, item_taken_count):
            items_taken = set(items_taken)

            pos_items = floors[pos] - items_taken
            if not is_valid(pos_items):
                continue

            next_pos_items = floors[next_pos] | items_taken
            if not is_valid(next_pos_items):
                continue

            next_floors = deepcopy(floors)
            next_floors[pos] = pos_items
            next_floors[next_pos] = next_pos_items

            possible_next_floors.append(next_floors)

    return possible_next_floors


def is_valid(items):
    generators = get_generator_materials(items)
    if not generators:
        return True

    microchips = get_microchip_materials(items)
    return microchips & generators == microchips


def run(floors):
    materials = list({
        material
        for floor_items in floors
        for material, _ in floor_items
    })

    floors = [
        {
            (
                materials.index(material),
                GENERATOR if item_type == 'generator' else MICROCHIP
            )
            for material, item_type in floor_items
        }
        for floor_items in floors
    ]

    def build_queue_entry(stops, pos, floors):
        # Min moves:
        # - Go back and forth between left-over floors
        # - Remove 1 trip for the current floor
        lower_bound = sum([
            2 * floor * math.ceil(len(floor_items) / 2)
            for floor, floor_items in enumerate(reversed(floors))
        ]) - pos

        return (
            lower_bound + stops,
            stops,
            pos,
            floors,
        )

    # If combinations are valid, we only care about the
    # number of microchips and generators per floor
    #
    # Materials are interchangeable
    def build_cache_key(pos, floors):
        floors_key = tuple([
            (
                len(get_microchip_materials(floor_items)),
                len(get_generator_materials(floor_items)),
            )
            for floor_items in floors
        ])
        return (pos, floors_key)

    queue = [build_queue_entry(0, 0, floors)]
    cache = set(build_cache_key(0, floors))
    min_stops = None
    while queue:
        _, stops, pos, floors = heapq.heappop(queue)

        if min_stops and min_stops <= stops:
            break

        if pos == 3 and not any(floors[:-1]):
            min_stops = safe_min(min_stops, stops)
            continue

        next_stops = stops + 1
        for next_pos in [pos - 1, pos + 1]:
            if not (0 <= next_pos <= 3):
                continue

            for next_floors in get_next_floors(floors, pos, next_pos):
                key = build_cache_key(next_pos, next_floors)
                if key in cache:
                    continue
                cache.add(key)

                heapq.heappush(
                    queue,
                    build_queue_entry(next_stops, next_pos, next_floors),
                )

    return min_stops

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
