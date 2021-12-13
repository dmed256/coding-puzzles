from repo_utils import *

input_lines = get_input_lines()

def run(problem, lines):
    grid = Grid(lines)

    objects = {}
    for pos, v in grid:
        if v in '#.':
            continue

        objects[v] = pos

    start_pos = objects['0']

    def find_shortest_path_distance(obj1, obj2):
        start_pos = objects[obj1]
        end_pos = objects[obj2]

        queue = [(start_pos, 0)]
        visited = set([start_pos])

        while queue:
            pos, steps = queue.pop(0)

            for npos in grid.neighbors(pos):
                if npos in visited:
                    continue

                if npos == end_pos:
                    return steps + 1

                v = grid[npos]

                if v == '#':
                    continue

                queue.append((npos, steps + 1))
                visited.add(npos)

    object_numbers = ''.join(sorted(objects.keys()))
    path_distances = {}

    for i in range(len(object_numbers)):
        obj1 = object_numbers[i]
        for j in range(i + 1, len(object_numbers)):
            obj2 = object_numbers[j]
            dist = find_shortest_path_distance(obj1, obj2)

            path_distances[(obj1, obj2)] = dist
            path_distances[(obj2, obj1)] = dist

    object_numbers = object_numbers.replace('0', '')

    queue = [(
        '0',
        object_numbers,
        0
    )]
    cache = set()

    min_steps = int(1e20)
    while queue:
        pos, missing_objects, steps = queue.pop(0)
        if min_steps <= steps:
            continue

        key = (pos, missing_objects, steps)
        if key in cache:
            continue
        cache.add(key)

        if not missing_objects:
            min_steps = min(min_steps, steps)
            continue

        for obj in missing_objects:
            dist = path_distances[(pos, obj)]
            next_missing_objects = missing_objects.replace(obj, '')

            # Need to return back
            if not next_missing_objects and problem == 2:
                dist += path_distances[(obj, '0')]

            queue.append((
                obj,
                next_missing_objects,
                steps + dist,
            ))

    return min_steps

example1 = multiline_lines(r"""
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
""")

run(1, example1) | eq(14)

run(1, input_lines) | debug('Star 1') | eq(428)

run(2, input_lines) | debug('Star 2') | eq(680)
