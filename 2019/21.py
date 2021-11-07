from advent_of_code import *
from int_processor import *

class Problem:
    def __init__(self):
        self.ascii_output = ''
        self.ascii_input = ''

    def get_input(self):
        while not self.ascii_input:
            if self.ascii_output:
                print(f'> {self.ascii_output}')
                self.ascii_output = ''

            ascii_input = input() + '\n'
            if not ascii_input.strip() or ascii_input.startswith('#'):
                continue

            self.ascii_input = [c for c in ascii_input]

        return ord(self.ascii_input.pop(0))

    def process_output(self, output):
        [code] = output

        if code >= 256:
            print(f'Code = {code}')
            return output

        self.ascii_output += chr(code)
        return []

    def run(self):
        input_value = get_input()
        p = IntProcessor(input_value)

        p.get_input = self.get_input
        p.process_output = self.process_output
        p.run()

        return self.ascii_output

# Star 1
"""
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
"""

# Star 2
"""
@ _ _ . _ . _ . _ .
0 1 2 3 4 5 6 7 8 9
  A B C D E F G H I

@ x _ _ x _
0 5 6 7 8 9
  E F G H I

. . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . .
# # # # # . # . # . # # . . # # #
  A B C D E F G H I

. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
J # # . J . # . # # . . # # #
  A B C D E F G H I

. . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . .
# # # # # . # # # . # . . . # # #
  A B C D E F G H I

. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
J # # . J # # . J . . . # # #
  A B C D E F G H I


if not A:
    return True
if D & (H | (E & (I OR F))) & !(B & C & D)
    return True


!(B & F & !H)
((!B || !F) || H)
(!(B && F) || H)

OR I T
OR F T
AND E T
OR H T
AND D T
OR T J

NOT B T
NOT T T
AND C T
AND D T
NOT T T
AND T J

NOT A T
OR T J

RUN
"""

Problem().run() | debug()
