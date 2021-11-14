import re
from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

PREFIX = 0
MIDDLE = 1
SUFFIX = 2

class Segment(BaseModel):
    index = 0

    prefixes = []
    middle = ''
    suffixes = []

    tier = -1
    original_value = ''
    compressed_value = ''

    def is_empty(self):
        return not bool(
            self.prefixes
            or self.middle
            or self.suffixes
        )

    def add(self, segment_type, value):
        if segment_type == PREFIX:
            self.prefixes.append(value)
        elif segment_type == MIDDLE:
            self.middle += value
        elif segment_type == SUFFIX:
            self.suffixes.append(value)

    def compress(self, inv_replacements, outputs):
        if self.tier >= 0:
            return self

        self.original_value = ''.join([
            *self.prefixes,
            self.middle,
            *self.suffixes,
        ])

        last_prefix = lget(self.prefixes, -1, '')
        first_suffix = lget(self.suffixes, 0, '')
        center = last_prefix + self.middle + first_suffix

        potential_outputs = [
            v
            for v in outputs
            if v in center
        ]
        if not potential_outputs:
            self.tier = 2
            self.compressed_value = self.original_value
            return self

        output = max(potential_outputs, key=len)

        self.tier = (
            0
            if center == output else
            1
        )

        self.prefixes = self.prefixes[:-1]
        self.suffixes = self.suffixes[1:]

        original = inv_replacements[output]
        if self.tier == 0:
            self.middle = original
        else:
            self.middle = center.replace(output, original, 1)

        self.compressed_value = ''.join([
            *self.prefixes,
            self.middle,
            *self.suffixes,
        ])

        return self

def parse_lines(lines):
    word = lines[-1]
    lines = lines[:-2]

    replacements = []
    for line in lines:
        [a, b] = line.split(' => ')
        replacements.append((a, b))

    return word, replacements

def find_replacements(word, c1, c2):
    replacements = set()
    for i in range(len(word)):
        if word[i:i+len(c1)] != c1:
            continue
        replacement = word[:i] + c2 + word[i+len(c1):]
        if replacement not in replacements:
            yield replacement
        replacements.add(replacement)

def find_combinations(word, replacements):
    combinations = set()
    for (c, c2) in replacements:
        combinations.update(
            find_replacements(word, c, c2)
        )
    return combinations

def run(lines):
    word, replacements = parse_lines(lines)
    return len(find_combinations(word, replacements))

example1 = multiline_lines(r"""
H => HO
H => OH
O => HH

HOH
""")

run(example1) | eq(4)
run(input_lines) | debug('Star 1') | eq(518)

class Problem():
    def __init__(self, lines):
        self.end_value, self.replacements = parse_lines(lines)

        self.inv_replacements = {
            c2: c1
            for c1, c2 in self.replacements
        }
        self.outputs = list(self.inv_replacements.keys())

        non_prefix = ' '.join([
            c2[1:]
            for c2 in self.outputs
        ])
        non_suffix = ' '.join([
            c2[:-1]
            for c2 in self.outputs
        ])

        self.prefixes = set()
        for c2 in self.outputs:
            for i in range(1, len(c2)):
                v = c2[:i]
                if v not in non_prefix:
                    self.prefixes.add(v)

        self.suffixes = set()
        for c2 in self.outputs:
            for i in range(1, len(c2)):
                v = c2[-i:]
                if v not in non_suffix:
                    self.suffixes.add(v)

        self.tags = {*self.prefixes, *self.suffixes}
        self.max_tag_length = len(max(self.tags, key=len))

    def find_next_word(self, value):
        words = []
        for i1 in range(0, len(value)):
            if words:
                break
            for i2 in range(i1, self.max_tag_length):
                v = value[i1: i2]
                if v in self.tags:
                    words.append(v)

        if not words:
            return value, ''

        next_word = max(words, key=len)
        if not value.startswith(next_word):
            # Did not find a prefix nor suffix
            next_word = value.split(next_word)[0]

        return next_word, value[len(next_word):]

    def compress(self, value):
        original_value = value

        word, next_value = self.find_next_word(value)
        if word == value:
            return self.brute_force_compress(value)

        value = next_value

        segments = [Segment(index=0)]
        segment_type = 0
        while word:
            if word in self.prefixes:
                next_segment_type = PREFIX
            elif word in self.suffixes:
                next_segment_type = SUFFIX
            else:
                next_segment_type = MIDDLE

            if next_segment_type < segment_type:
                segments.append(Segment(index=len(segments)))

            segment_type = next_segment_type
            segments[-1].add(segment_type, word)

            word, value = self.find_next_word(value)

        segments = [
            segment.compress(self.inv_replacements, self.outputs)
            for segment in segments
            if not segment.is_empty()
        ]
        if not segments:
            # Make sure we're not losing any characters
            assert not original_value
            return ''

        min_tier = min(s.tier for s in segments)
        steps_taken = len([
            s
            for s in segments
            if s.tier == min_tier
        ])
        self.steps += steps_taken

        # Make sure we captured all of the characters
        assert original_value == ''.join(
            s.original_value
            for s in segments
        )

        cool_prints = False
        if cool_prints:
            print(''.join(
                blue(s.original_value)
                if s.tier != min_tier else
                red(f'[{s.original_value}]')
                for s in segments
            ))
            print(f' [{steps_taken}/{self.steps}]-> ' + ''.join(
                blue(s.original_value)
                if s.tier != min_tier else
                yellow(f'[{s.compressed_value}]')
                for s in segments
            ))
            print()

        return ''.join(
            s.original_value
            if s.tier != min_tier else
            s.compressed_value
            for s in segments
        )

    def brute_force_compress(self, value):
        print(f'brute_force_compress({value})')
        raise 1

    def run(self):
        self.steps = 0

        value = self.end_value
        while value != 'e':
            value = self.compress(value)

        return self.steps

def run2(lines):
    return Problem(lines).run()

run2(input_lines) | debug('Star 2') | eq(200)
