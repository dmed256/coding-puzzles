from repo_utils import *

input_value = get_input()
input_lines = get_input_lines()

close = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

corrupt_pair_score = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

invalid_pair_score = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4,
}

def calc_incomplete_score(stack):
    score = 0
    for c in stack[::-1]:
        score = (score * 5) + invalid_pair_score[c]
    return score

def run(problem, lines):
    incomplete_scores = []
    corrupt_score = 0
    for line in lines:
        valid = True
        stack = []
        for c in line:
            if c in '([{<':
                stack.append(c)
            else:
                c2 = stack.pop()
                if c != close[c2]:
                    corrupt_score += corrupt_pair_score[c]
                    valid = False
                    break
        if valid:
            incomplete_scores.append(
                calc_incomplete_score(stack)
            )

    if problem == 1:
        return corrupt_score

    incomplete_scores = sorted(incomplete_scores)
    return incomplete_scores[len(incomplete_scores) // 2]

run(1, input_lines) | debug('Star 1') | eq(392043)

run(2, input_lines) | debug('Star 2') | eq(1605968119)
