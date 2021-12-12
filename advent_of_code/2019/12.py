import math
from repo_utils import *

def compare(v, other_v):
    if v == other_v:
        return 0
    return -1 if v > other_v else 1

def get_new_velocity(moons, moon_index):
    [pos, vel] = moons[moon_index]
    for i in range(4):
        if i == moon_index:
            continue
        [other_pos, other_vel] = moons[i]
        vel += compare(pos, other_pos)
    return vel

def apply_timestep(moons):
    velocities = [
        get_new_velocity(moons, i)
        for i in range(4)
    ]
    return [
        [moons[i][0] + velocity, velocity]
        for i, velocity in enumerate(velocities)
    ]

def split_moons(moons, axis):
    return [
        [moon[0][axis], moon[1][axis]]
        for moon in moons
    ]

def join_moons(moon_x, moon_y, moon_z):
    return [
        [[px, py, pz], [vx, vy, vz]]
        for [[px, vx], [py, vy], [pz, vz]] in zip(moon_x, moon_y, moon_z)
    ]

def init_moons(moon_positions):
    moons = [
        [pos, [0, 0, 0]]
        for pos in moon_positions
    ]
    return [
        split_moons(moons, axis)
        for axis in range(3)
    ]

def simulate(moon_positions, steps):
    [moon_x, moon_y, moon_z] = init_moons(moon_positions)

    for i in range(steps):
        moon_x = apply_timestep(moon_x)
        moon_y = apply_timestep(moon_y)
        moon_z = apply_timestep(moon_z)

    return join_moons(moon_x, moon_y, moon_z)

def get_energy(v):
    return sum(abs(x) for x in v)

def get_moon_energy(moon):
    [pos, vel] = moon
    return get_energy(pos) * get_energy(vel)

def get_system_energy(moons):
    return sum(
        get_moon_energy(moon)
        for moon in moons
    )

def run(moon_positions, steps):
    moons = simulate(moon_positions, steps)
    return get_system_energy(moons)

example1 = [
    [-1, 0, 2],
    [2, -10, -7],
    [4, -8, 8],
    [3, 5, -1],
]

example2 = [
    [-8, -10, 0],
    [5, 5, 10],
    [2, -7, 3],
    [9, -8, -3],
]

problem = [
    [16, -11, 2],
    [0, -4, 7],
    [6, 4, -10],
    [-3, -2, -4],
]

simulate(example1, 0) | eq([
    [[-1, 0, 2], [ 0, 0, 0]],
    [[ 2, -10, -7], [ 0, 0, 0]],
    [[ 4, -8, 8], [ 0, 0, 0]],
    [[ 3, 5, -1], [ 0, 0, 0]],
])

simulate(example1, 1) | eq([
    [[ 2, -1, 1], [ 3, -1, -1]],
    [[ 3, -7, -4], [ 1, 3, 3]],
    [[ 1, -7, 5], [-3, 1, -3]],
    [[ 2, 2, 0], [-1, -3, 1]],
])

simulate(example1, 2) | eq([
    [[ 5, -3, -1], [ 3, -2, -2]],
    [[ 1, -2, 2], [-2, 5, 6]],
    [[ 1, -4, -1], [ 0, 3, -6]],
    [[ 1, -4, 2], [-1, -6, 2]],
])

simulate(example1, 3) | eq([
    [[ 5, -6, -1], [ 0, -3, 0]],
    [[ 0, 0, 6], [-1, 2, 4]],
    [[ 2, 1, -5], [ 1, 5, -4]],
    [[ 1, -8, 2], [ 0, -4, 0]],
])

simulate(example1, 4) | eq([
    [[ 2, -8, 0], [-3, -2, 1]],
    [[ 2, 1, 7], [ 2, 1, 1]],
    [[ 2, 3, -6], [ 0, 2, -1]],
    [[ 2, -9, 1], [ 1, -1, -1]],
])

simulate(example1, 5) | eq([
    [[-1, -9, 2], [-3, -1, 2]],
    [[ 4, 1, 5], [ 2, 0, -2]],
    [[ 2, 2, -4], [ 0, -1, 2]],
    [[ 3, -7, -1], [ 1, 2, -2]],
])

simulate(example1, 6) | eq([
    [[-1, -7, 3], [ 0, 2, 1]],
    [[ 3, 0, 0], [-1, -1, -5]],
    [[ 3, -2, 1], [ 1, -4, 5]],
    [[ 3, -4, -2], [ 0, 3, -1]],
])

simulate(example1, 7) | eq([
    [[ 2, -2, 1], [ 3, 5, -2]],
    [[ 1, -4, -4], [-2, -4, -4]],
    [[ 3, -7, 5], [ 0, -5, 4]],
    [[ 2, 0, 0], [-1, 4, 2]],
])

simulate(example1, 8) | eq([
    [[ 5, 2, -2], [ 3, 4, -3]],
    [[ 2, -7, -5], [ 1, -3, -1]],
    [[ 0, -9, 6], [-3, -2, 1]],
    [[ 1, 1, 3], [-1, 1, 3]],
])

simulate(example1, 9) | eq([
    [[ 5, 3, -4], [ 0, 1, -2]],
    [[ 2, -9, -3], [ 0, -2, 2]],
    [[ 0, -8, 4], [ 0, 1, -2]],
    [[ 1, 1, 5], [ 0, 0, 2]],
])

simulate(example1, 10) | eq([
    [[ 2, 1, -3], [-3, -2, 1]],
    [[ 1, -8, 0], [-1, 1, 3]],
    [[ 3, -6, 1], [ 3, 2, -3]],
    [[ 2, 0, 4], [ 1, -1, -1]],
])

run(example1, 10) | eq(179)
run(example2, 100) | eq(1940)
run(problem, 1000) | debug('Star 1') | eq(10055)

def find_cycle(moons):
    position_hashes = set()
    while True:
        moons = apply_timestep(moons)
        pos_hash = tuple([
            *[pos for [pos, vel] in moons],
            *[vel for [pos, vel] in moons],
        ])
        if pos_hash in position_hashes:
            break

        position_hashes.add(pos_hash)

    return len(position_hashes)

def run2(moon_positions):
    [moon_x, moon_y, moon_z] = init_moons(moon_positions)

    cycle_x = find_cycle(moon_x)
    cycle_y = find_cycle(moon_y)
    cycle_z = find_cycle(moon_z)

    return math.lcm(cycle_x, cycle_y, cycle_z)

run2(example1) | eq(2772)
run2(example2) | eq(4686774924)
run2(problem) | debug('Star 2') | eq(374307970285176)
