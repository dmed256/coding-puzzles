from advent_of_code import *

input_lines = get_input_lines()

def run(lines):
    info = multiline_lines(r"""
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
    """.strip())
    info = {
        words[0]: int(words[1])
        for line in info
        if (words := line.split(': '))
    }

    sue1 = 0
    sue2 = 0
    for i, line in enumerate(input_lines):
        sue = i + 1
        words = [
            word
            for parts in line.split(': ')[1:]
            for word in parts.split(', ')
        ]

        item_count = len(words) // 2
        items = [words[i] for i in range(0, len(words), 2)]
        counts = [int(words[i]) for i in range(1, len(words), 2)]

        valid_items1 = 0
        valid_items2 = 0
        for item, count in zip(items, counts):
            expected_count = info[item]
            valid_items1 += count == expected_count
            if item in ('cats', 'trees'):
                valid_items2 += count > expected_count
            elif item in ('pomeranians', 'goldfish'):
                valid_items2 += count < expected_count
            else:
                valid_items2 += count == expected_count

        if valid_items1 == item_count:
            sue1 = sue
        if valid_items2 == item_count:
            sue2 = sue

        if sue1 and sue2:
            break

    return (sue1, sue2)

(sue1, sue2) = run(input_lines)

sue1 | debug('Star 1') | eq(103)
sue2 | debug('Star 2') | eq(405)
