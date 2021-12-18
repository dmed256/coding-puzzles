from repo_utils import *

input_lines = get_input_lines()


def is_int(v):
    return type(v) == int


def prepend_to_path(path, v):
    return tuple([v] + list(path))


def add_to_path(path, v):
    return tuple(list(path) + [v])


def pop_path(path):
    return tuple(list(path)[:-1])


def pretty_print(values):
    print(listify(values))


def listify(values):
    json_values = []
    for value, path in values:
        if is_int(value):
            path = path[:-1]

        node = json_values
        for entry_id in path:
            for _ in range(len(node), entry_id + 1):
                node.append([])
            node = node[entry_id]

        node.append(value)

    return json_values


def explode_values(values):
    for i in range(len(values) - 1):
        left, left_path = values[i]
        left_parent_path = pop_path(left_path)

        if len(left_parent_path) < 4:
            continue

        right, right_path = values[i + 1]
        right_parent_path = pop_path(right_path)

        if left_parent_path != right_parent_path:
            continue

        if 0 < i:
            value, path = values[i - 1]
            values[i - 1] = (value + left, path)
        if i < len(values) - 2:
            value, path = values[i + 2]
            values[i + 2] = (value + right, path)

        values[i] = (0, left_parent_path)
        values.pop(i + 1)

        return values, True

    return values, False


def split_values(values):
    for i in range(len(values)):
        node, path = values[i]

        if node < 10:
            continue

        left = node // 2
        right = node - left
        values[i] = (left, add_to_path(path, 0))
        values.insert(i + 1, (right, add_to_path(path, 1)))

        return values, True

    return values, False


def add(left, right):
    values = [
        (value, prepend_to_path(path, 0))
        for value, path in left
    ] + [
        (value, prepend_to_path(path, 1))
        for value, path in right
    ]

    changed = True
    while changed:
        values, changed = explode_values(values)
        if changed:
            continue

        values, changed = split_values(values)

    return values


def flatten_values(values, path):
    if is_int(values):
        return [(values, tuple(path))]

    cleaned_values = []
    for i, item in enumerate(values):
        cleaned_values += flatten_values(item, path + [i])

    return cleaned_values

def get_magnitude(value):
    if is_int(value):
        return value

    left, right = value
    return (
        (3 * get_magnitude(left))
        + (2 * get_magnitude(right))
    )


def run(problem, lines):
    values = [
        flatten_values(json.loads(line), [])
        for line in lines
    ]

    if problem == 1:
        value = values[0]
        for other in values[1:]:
            value = add(value, other)

        value = listify(value)
        return get_magnitude(value)

    max_value = 0
    for left, right in itertools.combinations(values, 2):
        value = add(left, right)
        value = listify(value)
        max_value = max(max_value, get_magnitude(value))

        value = add(right, left)
        value = listify(value)
        max_value = max(max_value, get_magnitude(value))

    return max_value


example1 = multiline_lines(r"""
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
""")

example2 = multiline_lines(r"""
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
""")

run(1, example1) | eq(3488)
run(1, example2) | eq(4140)

run(1, input_lines) | debug('Star 1') | eq(4243)

run(2, example2) | eq(3993)
run(2, input_lines) | debug('Star 2') | eq(4701)
