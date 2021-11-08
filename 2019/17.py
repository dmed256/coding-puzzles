from advent_of_code import *
from int_processor import *

class Program:
    def get_input(self):
        value = self.inputs.pop(0)
        return value

    def process_output(self, output):
        [code] = output

        if code >= 256:
            return output

        if code == ord('\n'):
            self.grid.append([])
        else:
            self.grid[-1].append(chr(code))

        return []

    def print_grid(self):
        print('\n'.join([
            ' '.join(line)
            for line in self.grid
        ]))

    def find_intersections(self):
        width  = len(self.grid[0])
        height = len(self.grid)

        return [
            (x, y)
            for y in range(1, height - 1)
            for x in range(1, width - 1)
            if self.grid[y][x] == '#' and 4 == len([
                    1
                    for (dx, dy) in DIRECTIONS
                    if self.grid[y + dy][x + dx] == '#'
            ])
        ]

    def print_robot_path(self):
        pos = self.robot_pos
        d = self.robot_direction

        width  = len(self.grid[0])
        height = len(self.grid)

        def get_grid_pos(pos, d):
            x = pos[0] + d[0]
            y = pos[1] + d[1]
            if (0 <= y < height) and (0 <= x < width):
                return self.grid[y][x]

        def get_potential_directions(pos):
            return [
                direction
                for direction in DIRECTIONS
                if get_grid_pos(pos, direction) == '#'
            ]

        path = [0]
        while True:
            (x, y) = pos

            # Keep the robot going
            if get_grid_pos(pos, d) in ['#', 'O']:
                path[-1] += 1

                if len(get_potential_directions(pos)) != 3:
                    self.grid[y][x] = '.'
                else:
                    self.grid[y][x] = '#'

                pos = apply_direction(pos, d)

                (x, y) = pos
                self.grid[y][x] = DIRECTION_TO_ASCII[d]
                continue

            # Find where to turn
            next_d = get_potential_directions(pos)
            if not next_d:
                break

            next_d = next_d[0]

            if CLOCKWISE[d] == next_d:
                path.append('R')
            else: # if COUNTER_CLOCKWISE[d] == next_d:
                path.append('L')
            path.append(0)

            d = next_d
            self.grid[y][x] = DIRECTION_TO_ASCII[d]

        print([n for n in path if n])

    def run_program(self, mode):
        self.loaded_grid = False
        self.grid = [[]]

        input_value = get_input()
        input_value = str(mode) + input_value[1:]

        self.p = IntProcessor(input_value)

        self.p.get_input = self.get_input
        self.p.process_output = self.process_output
        self.p.run()

        self.loaded_grid = True

        # Remove potential empty lines
        self.grid = [
            line
            for line in self.grid
            if line
        ]

        # Set the robot direction
        [self.robot_pos, self.robot_direction] = [
            [(x, y), direction]
            for (y, row) in enumerate(self.grid)
            for (x, v) in enumerate(row)
            if (direction := ASCII_TO_DIRECTION.get(v))
        ][0]

    def run(self):
        self.run_program(1)

        intersections = self.find_intersections()
        for (x, y) in intersections:
            self.grid[y][x] = 'O'

        return sum([
            x * y
            for (x, y) in intersections
        ])

    def run2(self):
        # path = [
        #     'L', 8, 'R', 12, 'R', 12, 'R', 10, A
        #     'R', 10, 'R', 12, 'R', 10,         B
        #     'L', 8, 'R', 12, 'R', 12, 'R', 10, A
        #     'R', 10, 'R', 12, 'R', 10,         B
        #     'L', 10, 'R', 10, 'L', 6,          C
        #     'L', 10, 'R', 10, 'L', 6,          C
        #     'R', 10, 'R', 12, 'R', 10,         B
        #     'L', 8, 'R', 12, 'R', 12, 'R', 10, A
        #     'R', 10, 'R', 12, 'R', 10,         B
        #     'L', 10, 'R', 10, 'L', 6,          C
        # ]

        main_movement_routine = [
            'A', 'B', 'A', 'B', 'C', 'C', 'B', 'A', 'B', 'C',
        ]
        main_movement_functions = [
            ['L', 8, 'R', 12, 'R', 12, 'R', 10],
            ['R', 10, 'R', 12, 'R', 10],
            ['L', 10, 'R', 10, 'L', 6],
        ]

        inputs = '\n'.join([
            ','.join(main_movement_routine),
            *[
                ','.join([str(n) for n in main_movement_function])
                for main_movement_function in main_movement_functions
            ],
            'n',
            '',
        ])
        self.inputs = [ord(c) for c in inputs]

        self.run_program(2)
        return self.p.output[0]


program = Program()

program.run() | debug('Star 1') | eq(4372)

program.run2() | debug('Star 2') | eq(945911)
