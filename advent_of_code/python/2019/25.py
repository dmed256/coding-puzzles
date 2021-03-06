import re
from repo_utils import *
from int_processor import *

W = 20
D = 2*W + 1

items = [
    'space law space brochure',
    'mouse',
    'astrolabe',
    'mug',
    'sand',
    'monolith',
    'manifold',
    'wreath',
]

class Problem:
    def __init__(self):
        self.ascii_output = ''
        self.ascii_input = [
            c
            for c in textwrap.dedent(multiline_input("""
            south
            take space law space brochure
            south
            take mouse
            west
            north
            north
            take wreath
            south
            south
            east
            south
            take astrolabe
            south
            take mug
            north
            north
            north
            west
            take sand
            west
            take monolith
            east
            north
            take manifold
            south
            west
            west
            drop space law space brochure
            drop mouse
            drop astrolabe
            drop mug
            drop sand
            drop monolith
            drop manifold
            drop wreath
            """))
        ]

        self.item_combination = 0

    def get_input(self):
        self.load_auto_input()

        return ord(self.ascii_input.pop(0))

    def load_human_input(self):
        while not self.ascii_input:
            if self.ascii_output:
                print(f'> {self.ascii_output}')
                self.ascii_output = ''

            ascii_input = input() + '\n'
            if not ascii_input.strip() or ascii_input.startswith('#'):
                continue

            self.ascii_input = [c for c in ascii_input]

    def load_auto_input(self):
        while not self.ascii_input:
            self.ascii_output = ''

            ascii_input = ''
            self.item_combination += 1
            if self.item_combination:
                v1 = self.item_combination - 1
                v2 = self.item_combination
                for i, item in enumerate(items):
                    if v1 & 2**i == v2 & 2**i:
                        continue
                    if v1 & 2**i:
                        ascii_input += f'drop {items[i]}\n'
                    else:
                        ascii_input += f'take {items[i]}\n'
            ascii_input += 'west\n'

            self.ascii_input = [c for c in ascii_input]

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

        password = re.search(
            'You should be able to get in by typing (\d+) on the keypad at the main airlock',
            self.ascii_output,
        ).groups()[0]

        return int(password)

Problem().run() | debug('Star 1') | eq(328960)
