from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

class Problem:
    def __init__(self, problem, lines):
        self.problem = problem
        self.lines = lines

    def is_valid(self, line):
        words = line.split(' ')
        seen_words = set()
        for word in words:
            if word in seen_words:
                return False
            seen_words.add(word)

        if self.problem == 2:
            return self.is_valid2(words)

        return True

    def is_valid2(self, words):
        seen_charsets = set()
        for word in words:
            word = tuple(sorted(word))
            if word in seen_charsets:
                return False
            seen_charsets.add(word)
        return True

    def run(self):
        return len([
            1
            for line in self.lines
            if self.is_valid(line)
        ])

def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

run(['aa bb cc dd ee']) | eq(1)
run(['aa bb cc dd aa']) | eq(0)
run(['aa bb cc dd aaa']) | eq(1)

run(input_lines) | debug('Star 1') | eq(455)

run2(['abcde fghij']) | eq(1)
run2(['abcde xyz ecdab']) | eq(0)
run2(['a ab abc abd abf abj']) | eq(1)
run2(['iiii oiii ooii oooi oooo']) | eq(1)
run2(['oiii ioii iioi iiio']) | eq(0)

run2(input_lines) | debug('Star 2') | clipboard()
