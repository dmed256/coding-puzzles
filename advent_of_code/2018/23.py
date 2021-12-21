from repo_utils import *

input_lines = get_input_lines()

Rect = namedtuple('Rect', ['pos', 'size'])

# We're going to rotate the coordinates so we're looking at prisms
# rather than weird diamonds
#
# . . . . . . .    . . . . . . .
# . . . # . . .    . # # # # # .
# . . # # # . .    . # # # # # .
# . # # # # # . -> . # # # # # .
# . . # # # . .    . # # # # # .
# . . . # . . .    . # # # # # .
# . . . . . . .    . . . . . . .
#
# The corners map to:
#
#   (-2,  0, 0) <-> (-2, -2,  0)
#   ( 0,  2, 0) <-> (-2,  2,  0)
#   ( 0, -2, 0) <-> ( 0, -2, -2)
#   ( 0,  0, 2) <-> ( 0, -2,  2)
#   (-2,  0, 0) <-> (-2,  0, -2)
#   ( 0,  0, 2) <-> (-2,  0,  2)
#
#   ->
#   [  1, -1,  0 ] [ -1,  0,  0 ]   [ -1, -1,  0 ]
#   [  1,  1,  0 ] [  0,  1,  0 ] = [ -1,  1,  0 ]
#   [  0, -1,  1 ] [  0,  0,  1 ]   [  0, -1,  1 ]
#
#   <-
#   [  1, -1,  0 ] -1         [  1  1  0 ]
#   [  1,  1,  0 ]    = 0.5 * [ -1  1  0 ]
#   [  0, -1,  1 ]            [ -1  1  2 ]
#
def run(problem, lines):
    rects = []
    for line in lines:
        left, r = line.split('>, r=')

        r = int(r)
        x, y, z = [int(x) for x in left.split('<')[1].split(',')]

        # Apply rotation matrix
        pos2 = [x - y, x + y, -y + z]

        # The width is actually r * sqrt(2) but the scaling doesn't matter
        rects.append(Rect(pos2, r))

    pass

example1 = multiline_lines(r"""
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1
""")

run(1, example1) | eq(7)

run(1, input_lines) | debug('Star 1') | eq(305)

example2 = multiline_lines(r"""
pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5
""")

# run(2, example2) | eq(36)

# run(2, input_lines) | debug('Star 2')
