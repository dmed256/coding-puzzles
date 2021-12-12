from repo_utils import *

input_value = get_input()
input_lines = get_input_lines()

class Problem:
    def __init__(self, problem, lines):
        self.problem = problem

        tiles = {}
        for line in lines:
            nav = [
                s
                for s in re.split('(s[ew]|n[ew]|.)', line)
                if s
            ]
            x = 0
            y = 0
            for s in nav:
                if s == 'e':
                    x += 2
                elif s == 'se':
                    x += 1
                    y -= 1
                elif s == 'sw':
                    x -= 1
                    y -= 1
                elif s == 'w':
                    x -= 2
                elif s == 'nw':
                    x -= 1
                    y += 1
                elif s == 'ne':
                    x += 1
                    y += 1
            pos = (x, y)
            if pos in tiles:
                tiles[pos] = not tiles[pos]
            else:
                tiles[pos] = True

        self.tiles = tiles

    def get_neighbors(self, pos):
        x, y = pos
        return [
            (x - 2, y),
            (x + 2, y),
            (x - 1, y - 1),
            (x + 1, y - 1),
            (x - 1, y + 1),
            (x + 1, y + 1),
        ]

    def get_black_neighbor_count(self, pos, flipped_tiles):
        return len([
            1
            for neighbor in self.get_neighbors(pos)
            if neighbor in flipped_tiles
        ])

    def run(self):
        flipped_tiles = {
            pos
            for pos, flipped in self.tiles.items()
            if flipped
        }

        days = 0 if self.problem == 1 else 100

        for i in range(days):
            next_flipped_tiles = set()
            for tile in flipped_tiles:
                black_neighbors = self.get_black_neighbor_count(tile, flipped_tiles)
                if 1 <= black_neighbors <= 2:
                    next_flipped_tiles.add(tile)

            neighbor_white_tiles = {
                neighbor
                for tile in flipped_tiles
                for neighbor in self.get_neighbors(tile)
                if neighbor not in flipped_tiles
            }
            next_flipped_tiles |= {
                tile
                for tile in neighbor_white_tiles
                if 2 == self.get_black_neighbor_count(tile, flipped_tiles)
            }
            flipped_tiles = next_flipped_tiles

        return len(flipped_tiles)


def run(*args):
    return Problem(1, *args).run()

def run2(*args):
    return Problem(2, *args).run()

example1 = multiline_lines(r"""
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
""")

run(example1) | eq(10)

run(input_lines) | debug('Star 1') | eq(523)

run2(example1) | eq(2208)

run2(input_lines) | debug('Star 2') | eq(4225)
