from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

Borders = namedtuple('Borders', ['top', 'right', 'bottom', 'left'])

class Problem:
    def __init__(self, problem, lines):
        self.problem = problem

        def get_ordered_border(border):
            return min(border, border[::-1])

        def get_borders(tile):
            return Borders(
                top=get_ordered_border(
                    tile[0]
                ),
                right=get_ordered_border(
                    ''.join((row[-1] for row in tile))
                ),
                bottom=get_ordered_border(
                    tile[-1]
                ),
                left=get_ordered_border(
                    ''.join((row[0] for row in tile))
                ),
            )

        tiles = {}
        for i in range(0, len(lines), 12):
            tile_id = int(lines[i][:-1].split(' ')[1])
            tile = lines[i+1:i+11]
            borders = get_borders(tile)
            tiles[tile_id] = [tile, borders]

        size = math.isqrt(len(tiles))
        tile_size = len(tile[0])

        border_ids = {}
        for tile_id, [_, borders] in tiles.items():
            for border in [borders.top, borders.right, borders.bottom, borders.left]:
                if border not in border_ids:
                    border_ids[border] = set()
                    border_ids[border[::-1]] = set()
                border_ids[border].add(tile_id)
                border_ids[border[::-1]].add(tile_id)

        links = {}
        for tile_ids in border_ids.values():
            tile_ids = list(tile_ids)
            for i in range(len(tile_ids)):
                ti = tile_ids[i]
                if ti not in links:
                    links[ti] = set()
                for j in range(i + 1, len(tile_ids)):
                    tj = tile_ids[j]
                    if tj not in links:
                        links[tj] = set()
                    links[ti].add(tj)
                    links[tj].add(ti)

        # Corners have 2 links
        # Edges have 3 links
        # Center tiles have 4 links
        corner = [
            tile_id
            for tile_id, tile_links in links.items()
            if len(tile_links) == 2
        ][0]

        # Create the first row by finding 1 corner and connecting
        # tiles 1 by 1
        row1 = [corner]
        for c in range(1, size):
            prev_tile_id = row1[c - 1]
            row1.append(
                [
                    tile_link
                    for tile_link in links[prev_tile_id]
                    if len(links[tile_link]) < 4
                    and tile_link not in row1
                ][0]
            )

        # Create image rows by finding the only missing link
        # from the row above it
        image_ids = [row1]
        used_ids = set(row1)
        for r in range(1, size):
            prev_row = image_ids[r - 1]
            next_row = [
                link_id
                for tile_id in prev_row
                for link_id in set(links[tile_id]) - used_ids
            ]
            used_ids |= set(next_row)
            image_ids.append(next_row)

        def align_tile(r, c):
            tile_id = image_ids[r][c]

            top_id, right_id, bottom_id, left_id = None, None, None, None
            if 0 <= r - 1:
                top_id = image_ids[r - 1][c]
            if r + 1 < size:
                bottom_id = image_ids[r + 1][c]
            if 0 <= c - 1:
                left_id = image_ids[r][c - 1]
            if c + 1 < size:
                right_id = image_ids[r][c + 1]

            [tile, _] = tiles[tile_id]
            for tile in self.get_arrangements(tile):
                borders = get_borders(tile)
                is_valid = all((
                    border_id in linked_ids
                    if border_id else
                    {tile_id} == linked_ids
                    for border_id, linked_ids in [
                        (top_id, border_ids[borders.top]),
                        (right_id, border_ids[borders.right]),
                        (bottom_id, border_ids[borders.bottom]),
                        (left_id, border_ids[borders.left]),
                    ]
                ))
                if is_valid:
                    tiles[tile_id] = tile
                    break

        for r in range(size):
            for c in range(size):
                align_tile(r, c)

        image = []
        for r in range(size):
            for rt in range(1, tile_size - 1):
                row = ''
                for c in range(size):
                    for ct in range(1, tile_size - 1):
                        row += tiles[image_ids[r][c]][rt][ct]
                image.append(row)

        self.size = size
        self.tiles = tiles
        self.links = links
        self.image_ids = image_ids
        self.image = image
        self.image_size = len(self.image)

    def print_tile(self, tile):
        print('\n'.join(tile))

    def get_arrangements(self, tile):
        options = []
        for flips in range(2):
            for rotations in range(4):
                options.append(tile)
                tile = self.rotate_right(tile)
            tile = self.flip(tile)
        return options

    @staticmethod
    def rotate_right(img):
        height = len(img)
        width = len(img[0])

        return [
            ''.join(
                img[height - c - 1][r]
                for c in range(height)
            )
            for r in range(width)
        ]

    @staticmethod
    def flip(img):
        return img[::-1]

    def get_hash_points(self, image):
        return set([
            (r, c)
            for r, row in enumerate(image)
            for c, char in enumerate(row)
            if char == '#'
        ])

    def run(self):
        if self.problem == 1:
            return mult([
                self.image_ids[0][0],
                self.image_ids[0][-1],
                self.image_ids[-1][0],
                self.image_ids[-1][-1],
            ])

        monster = [
            '                  # ',
            '#    ##    ##    ###',
            ' #  #  #  #  #  #   ',
        ]

        def mark_monster_points(image, r, c, marked_monster_points):
            image_monster_points = set([
                (r + dr, c + dc)
                for dr, dc in monster_points
            ])
            is_monster = all(
                image[ir][ic] == '#'
                for ir, ic in image_monster_points
            )
            if is_monster:
                marked_monster_points |= image_monster_points

        marked_monster_points = set()
        for monster_img in self.get_arrangements(monster):
            monster_points = self.get_hash_points(monster_img)
            monster_height = len(monster_img)
            monster_width = len(monster_img[0])

            for r in range(0, self.image_size - monster_height + 1):
                for c in range(0, self.image_size - monster_width + 1):
                    mark_monster_points(self.image, r, c, marked_monster_points)

        return len(
            self.get_hash_points(self.image) - marked_monster_points
        )

def run(lines):
    return Problem(1, lines).run()

def run2(lines):
    return Problem(2, lines).run()

example1 = multiline_lines(r"""
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
""")

run(example1) | eq(20899048083289)

run(input_lines) | debug('Star 1') | eq(20913499394191)

run2(example1) | eq(273)

run2(input_lines) | debug('Star 2') | eq(2209)
