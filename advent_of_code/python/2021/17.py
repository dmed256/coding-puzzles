from repo_utils import *


# Formula for finding positions given an initial velocity (vx, vy)
# and some time t
#
# t   0     1          2       ... t
# x = vx + (vx - 1) + (vx - 2) ... (vx - min(t, vx))
# y = vy + (vy - 1) + (vy - 2) ... (vy - t)
def get_x_position(vx, t):
    t = min(vx, t)
    return ((vx + (vx - t)) * (t + 1)) // 2


def get_y_position(vy, t):
    return ((vy + (vy - t)) * (t + 1)) // 2


def run(problem, area):
    x_range, y_range = area
    x_min, x_max = x_range
    y_min, y_max = y_range

    # 0 can't be in x_range otherwise there are infinite solutions
    if x_min < 0 and x_max < 0:
        # Mirror to the positive x-axis range
        x_min, x_max = -x_max, -x_min

    # Doesn't make sense for vx to be negative since x_range is positive
    # -> min(vx) == 1
    #
    # We can't go over the area in 1 time step
    # -> max(vx) == x_max
    valid_vx = []
    for vx in range(1, x_max + 1):
        for t in range(vx + 1):
            x = get_x_position(vx, t)
            if x_max < x:
                break

            if x_min <= x <= x_max:
                is_terminal_vx = t == vx
                valid_vx.append((vx, t, is_terminal_vx))

    velocity_flight_times = {}
    for vx, min_t, is_terminal_vx in valid_vx:
        # If is_terminal_vx, the probe will stop moving in the x-axis
        # but can still move in the y-axis
        if is_terminal_vx:
            max_t = min_t + 1000000
        else:
            max_t = min_t + 1

        # Probably a smarter way to find the range here
        for vy in range(-1000, 1000):
            for t in range(min_t, max_t):
                y = get_y_position(vy, t)

                if y < y_min:
                    break

                if y_min <= y <= y_max:
                    velocity_flight_times[(vx, vy)] = safe_max(
                        t,
                        velocity_flight_times.get((vx, vy)),
                    )

    max_height = 0
    for (vx, vy), max_t in velocity_flight_times.items():
        # After t reaches vy, the probe starts going down
        peak_t = min(max_t, vy)
        max_height = max(
            max_height,
            get_y_position(vy, peak_t),
        )

    if problem == 1:
        return max_height
    else:
        return len(velocity_flight_times)

run(1, [(20, 30), (-10, -5)]) | eq(45)

run(1, [(34, 67), (-215, -186)]) | debug('Star 1') | eq(23005)

run(2, [(20, 30), (-10, -5)]) | eq(112)

run(2, [(34, 67), (-215, -186)]) | debug('Star 2') | eq(2040)
