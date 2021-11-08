from advent_of_code import *
from int_processor import *

class Problem:
    def __init__(self, solution):
        self.ascii_output = ''
        self.ascii_input = [
            c
            for line in solution.splitlines()
            if line and not line.startswith('#')
            for c in (line + '\n')
        ]
        self.hull_damage = 0

    def get_input(self):
        return ord(self.ascii_input.pop(0))

    def process_output(self, output):
        [code] = output

        if code >= 256:
            self.hull_damage = code
            return output

        self.ascii_output += chr(code)
        return []

    def run(self):
        input_value = get_input()
        p = IntProcessor(input_value)

        p.get_input = self.get_input
        p.process_output = self.process_output
        p.run()

        return self.hull_damage

solution1 = multiline_input("""
# If there's no floor in the next time, JUMP!
NOT A J

# Jump if there is a space to jump
OR D J

# Check if all 4 tiles have floor, if they do DON'T JUMP YET!
OR A T
AND B T
AND C T
AND D T

# !(DON'T JUMP) -> Maybe jump...
NOT T T
AND T J
WALK
""")

solution2 = multiline_input("""
# if D & (H | (E & (I OR F))) & !(B & C & D)
#     return True#
#
# !(B & F & !H)
# ((!B || !F) || H)
# (!(B && F) || H)
OR I T
OR F T
AND E T
OR H T
AND D T
OR T J

# !(B & C & D)
NOT B T
NOT T T
AND C T
AND D T
NOT T T
AND T J

# if not A:
#     return True
NOT A T
OR T J

RUN
""")

Problem(solution1).run() | debug('Star 1') | eq(19354083)

Problem(solution2).run() | debug('Star 2') | eq(1143499964)
