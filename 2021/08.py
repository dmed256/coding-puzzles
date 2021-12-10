from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

def key(v):
    return tuple(sorted(v))

base_digits = {
    'abcefg': 0,
    'cf': 1,
    'acdeg': 2,
    'acdfg': 3,
    'bcdf': 4,
    'abdfg': 5,
    'abdefg': 6,
    'acf': 7,
    'abcdefg': 8,
    'abcdfg': 9,
}

base_digit_keys = {
    key(k)
    for k in base_digits.keys()
}

def find_digit_map(patterns):
    letters = 'abcdefg'
    for perm in itertools.permutations('abcdefg'):
        letter_map = {
            c1: c2
            for c1, c2 in zip(perm, letters)
        }
        for pattern in patterns:
            k = key(''.join(letter_map[c] for c in pattern))
            found = k in base_digit_keys
            if not found:
                break
        if found:
            break

    inv_letter_map = {
        c2: c1
        for c1, c2 in letter_map.items()
    }
    return {
        key(inv_letter_map[c] for c in k): digit
        for k, digit in base_digits.items()
    }

def run(problem, lines):
    count = 0
    p2 = 0
    for line in lines:
        [left, right] = line.split(' | ')
        patterns = left.split(' ')
        outputs = right.split(' ')

        digit_map = find_digit_map(patterns)

        digit = ''
        for output in outputs:
            digit += str(digit_map[key(output)])
            if len(output) in [2, 3, 4, 7]:
                count += 1
        p2 += int(digit)

    if problem == 1:
        return count

    return p2



example1 = multiline_lines(r"""
acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
""")

example2 = multiline_lines(r"""
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
""")

run(1, input_lines) | debug('Star 1') | eq(274)

run(2, example1) | eq(5353)
run(2, example2) | eq(61229)

run(2, input_lines) | debug('Star 2') | eq(1012089)
