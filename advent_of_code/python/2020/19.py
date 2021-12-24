from repo_utils import *

input_value = get_input()
input_lines = get_input_lines()

def word_breakdowns(word, parts):
    if parts == 1:
        return [[word]]

    return [
        [word[:i]] + other
        for i in range(1, len(word) - parts + 2)
        for other in word_breakdowns(word[i:], parts - 1)
    ]

class Problem:
    def __init__(self, lines, problem):
        self.problem = problem

        for i, line in enumerate(lines):
            if not line.strip():
                break

        rule_lines = lines[:i]
        words = lines[i+1:]

        rules = {}
        for line in rule_lines:
            key, output = line.split(': ')
            key = int(key)

            const_split = output.split('"')
            if len(const_split) > 1:
                rules[key] = const_split[1]
                continue

            outputs = output.split(' | ')
            outputs = [
                [int(x) for x in output.split(' ')]
                for output in outputs
            ]
            rules[key] = outputs

        rule_deps = {
            rule: set([
                v
                for expansion in expansions
                for v in expansion
            ])
            for rule, expansions in rules.items()
        }

        const_rules = [
            rule
            for rule, expansions in rules.items()
            if len(expansions) == 1 and type(expansions[0]) is str
        ]

        rule_ranges = {
            const_rule: [1, 1]
            for const_rule in const_rules
        }
        found_rule_ranges = set(rule_ranges.keys())
        missing_rule_ranges = set(rules.keys()) - found_rule_ranges
        while missing_rule_ranges:
            found = set()
            for rule in missing_rule_ranges:
                if not (rule_deps[rule] <= found_rule_ranges):
                    continue

                found.add(rule)
                rule_range = [23894032894, 0]
                for expansion in rules[rule]:
                    rng = [
                        sum(rule_ranges[r][0] for r in expansion),
                        sum(rule_ranges[r][1] for r in expansion),
                    ]
                    rule_range = [
                        min(rule_range[0], rng[0]),
                        max(rule_range[1], rng[1]),
                    ]
                rule_ranges[rule] = rule_range

            found_rule_ranges |= found
            missing_rule_ranges -= found

        self.rules = rules
        self.rule_ranges = rule_ranges
        self.rule_deps = rule_deps
        self.words = words

    def is_valid8(self, word):
        if self.is_valid(word, 42):
            return True

        for [left, right] in word_breakdowns(word, 2):
            if (self.is_valid(left, 42) and
                self.is_valid8(right)):
                return True

        return False

    def is_valid11(self, word):
        for [left, right] in word_breakdowns(word, 2):
            if (self.is_valid(left, 42) and
                self.is_valid(right, 31)):
                return True

        for [left, mid, right] in word_breakdowns(word, 3):
            if (self.is_valid(left, 42) and
                self.is_valid(right, 31) and
                self.is_valid11(mid)):
                return True

        return False

    def is_valid(self, word, match_rule):
        if type(match_rule) is str:
            return word == match_rule

        key = (word, match_rule)
        if key in self.cache:
            return self.cache[key]

        recusive_rules = set([8, 11])
        if self.problem == 2 and match_rule in recusive_rules:
            if match_rule == 8:
                valid = self.is_valid8(word)
            else:
                valid = self.is_valid11(word)
            self.cache[key] = valid
            return valid

        rule_range = self.rule_ranges[match_rule]
        if (recusive_rules ^ self.rule_deps[match_rule]
            and not (rule_range[0] <= len(word) <= rule_range[1])):
            self.cache[key] = False
            return False

        options = [
            [
                (new_word, new_match_rule)
                for new_word, new_match_rule in zip(breakdown, expansion)
            ]
            for expansion in self.rules[match_rule]
            for breakdown in word_breakdowns(word, len(expansion))
        ]
        valid = any((
            all((
                self.is_valid(new_word, new_match_rule)
                for new_word, new_match_rule in option
            ))
            for option in options
        ))
        self.cache[key] = valid
        return valid

    def run(self):
        self.cache = {}
        return len([
            1
            for word in self.words
            if self.is_valid(word, 0)
        ])

def run(lines):
    return Problem(lines, 1).run()

def run2(lines):
    return Problem(lines, 2).run()

example1 = multiline_lines(r"""
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
""")

example2 = multiline_lines(r"""
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
""")

run(example1) | eq(2)
run(example2) | eq(3)
run(input_lines) | debug('Star 1') | eq(250)

run2(example2) | eq(12)
run2(input_lines) | debug('Star 2') | eq(359)
