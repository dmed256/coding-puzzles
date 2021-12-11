from advent_of_code import *

input_lines = get_input_lines()

def run(problem, lines, chips=None):
    chips = chips and tuple(sorted(chips))
    values = defaultdict(list)

    while lines:
        unused_lines = []
        for line in lines:
            parts = line.split()

            if parts[0] == 'value':
                value = int(parts[1])
                key = ' '.join(parts[-2:])
                values[key].append(value)
                continue

            key = ' '.join(parts[:2])
            key_values = sorted(values[key])
            if len(key_values) < 2:
                unused_lines.append(line)
                continue

            out1 = ' '.join(parts[5:7])
            out2 = ' '.join(parts[-2:])
            low, high = key_values

            values[out1].append(low)
            values[out2].append(high)

        lines = unused_lines

    if problem == 1:
        for key, key_chips in values.items():
            if chips == tuple(sorted(key_chips)):
                return int(
                    key.replace('bot ', '')
                )

    return mult(
        value
        for i in range(3)
        for value in values[f'output {i}']
    )

example1 = multiline_lines(r"""
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
""")

run(1, example1, (2, 5)) | eq(2)

run(1, input_lines, (17, 61)) | debug('Star 1') | eq(161)

run(2, input_lines) | debug('Star 2') | eq(133163)
