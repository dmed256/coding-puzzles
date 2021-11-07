from advent_of_code import *
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
            for c in (multiline_input("""
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
            west
            drop space law space brochure
            drop mouse
            drop astrolabe
            drop mug
            drop sand
            drop monolith
            drop manifold
            drop wreath
            """) + '\n')
        ]

        self.item_combination = 0

    def get_input(self):
        return self.get_auto_input()

    def get_human_input(self):
        while not self.ascii_input:
            if self.ascii_output:
                print(f'> {self.ascii_output}')
                self.ascii_output = ''

            ascii_input = input() + '\n'
            if not ascii_input.strip() or ascii_input.startswith('#'):
                continue

            self.ascii_input = [c for c in ascii_input]

        return ord(self.ascii_input.pop(0))

    def get_auto_input(self):
        while not self.ascii_input:
            if self.ascii_output:
                if (('heavier' not in self.ascii_output) and
                    ('lighter' not in self.ascii_output)):
                    print(f'> {self.ascii_output}')
                    for i, item in enumerate(items):
                        if self.item_combination & 2**i:
                            print(f'TAKE {item}!!')
                    raise 1

                self.ascii_output = ''

            self.item_combination += 1
            print(self.item_combination)
            ascii_input = ''
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

Problem().run() | debug()
