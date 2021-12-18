from repo_utils import *

input_lines = get_input_lines()

def run(problem, lines, message_t=None):
    coords = []
    for line in lines:
        x, y, vx, vy = [
            int(item)
            for item in (
                    line
                    .replace('position=', '')
                    .replace(' velocity=', ',')
                    .replace(' ', '')
                    .replace('<', '')
                    .replace('>', '')
                    .split(',')
            )
        ]
        coords.append((x, y, vx, vy))

    def print_grid(t, coords):
        min_x = min(coord[0] for coord in coords)
        max_x = max(coord[0] for coord in coords)

        min_y = min(coord[1] for coord in coords)
        max_y = max(coord[1] for coord in coords)

        if max(max_x - min_x, max_y - min_y) >= 100:
            return

        points = [
            (coord[0] - min_x, coord[1] - min_y)
            for coord in coords
        ]

        print(f't = {t}')
        Grid.from_points(points).print()

    max_t = message_t + 1 if message_t else 10000000000
    for t in range(1, max_t):
        coords = [
            (x + vx, y + vy, vx, vy)
            for x, y, vx, vy in coords
        ]

        if not message_t:
            print_grid(t, coords)
        elif t == message_t:
            # We know when to print
            print_grid(t, coords)

    return None

example1 = multiline_lines(r"""
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
""")

run(1, example1, 3)

run(1, input_lines, 10813)

'ERCXLAJL' | debug('Star 1')

10813 | debug('Star 2')
