from advent_of_code import *

def parse_line(line):
    line = line.replace(' bags', '')
    line = line.replace(' bag', '')
    # Remove .
    line = line[:-1]

    [bag, contents] = line.split(' contain ')
    deps = []

    if contents != 'no other':
        for content in contents.split(', '):
            words = content.split(' ')
            deps.append([int(words[0]), ' '.join(words[1:])])

    return [bag, deps]


def find_bag_contents(bag, deps, bags):
    if bag in bags:
        return bags[bag]

    contents = {}
    for count, inner_bag in deps[bag]:
        contents[inner_bag] = (
            contents.get(inner_bag, 0)
            + count
        )
        for inner_inner_bag, inner_inner_count in find_bag_contents(inner_bag, deps, bags).items():
            contents[inner_inner_bag] = (
                contents.get(inner_inner_bag, 0)
                + (count * inner_inner_count)
            )

    bags[bag] = contents
    return contents

def run(lines, problem):
    deps = {}
    for line in lines:
        [bag, bag_deps] = parse_line(line)
        deps[bag] = bag_deps

    bags = {}
    for bag in set(deps.keys()):
        find_bag_contents(bag, deps, bags)

    if problem == 1:
        return len([
            1
            for bag, contents in bags.items()
            if 'shiny gold' in contents
        ])

    return sum([
        count
        for count in bags['shiny gold'].values()
    ])

example1 = multiline_lines(r"""
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
""")

run(example1, 1) | eq(4)

input_lines = get_input_lines()

run(input_lines, 1) | debug('Star 1') | eq(192)

example2 = multiline_lines(r"""
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
""")

run(example2, 2) | eq(126)

run(input_lines, 2) | debug('Star 2') | eq(12128)
