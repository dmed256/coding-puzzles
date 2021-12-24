from repo_utils import *

def run(players, last_marble):
    left_node  = [0] * (last_marble + 1)
    right_node = [0] * (last_marble + 1)

    def go_right(ptr, n):
        for _ in range(n):
            ptr = right_node[ptr]
        return ptr

    def go_left(ptr, n):
        for _ in range(n):
            ptr = left_node[ptr]
        return ptr

    def add_marble(ptr, marble):
        ptr = go_right(ptr, 2)

        # left -> [ptr] -> right
        left = left_node[ptr]
        right = right_node[ptr]

        # left -> [marble] -> [ptr] -> right
        right_node[left] = marble

        left_node[marble] = left
        right_node[marble] = ptr

        left_node[ptr] = marble

        return marble

    def remove_marble(ptr, marble):
        ptr = go_left(ptr, 7)

        # left -> [ptr] -> right
        # left ->  right
        left = left_node[ptr]
        right = right_node[ptr]

        right_node[left] = right
        left_node[right] = left

        return right, (ptr + marble)

    player_scores = [0] * players

    ptr = 0
    player = 0
    for marble in range(1, last_marble + 1):
        if marble % 23:
            ptr = add_marble(ptr, marble)
        else:
            ptr, score = remove_marble(ptr, marble)
            player_scores[player] += score

        player = (player + 1) % players

    return max(player_scores)

run(9, 25) | eq(32)
run(10, 1618) | eq(8317)
run(13, 7999) | eq(146373)
run(17, 1104) | eq(2764)
run(21, 6111) | eq(54718)
run(30, 5807) | eq(37305)

run(427, 70723) | debug('Star 1') | eq(399745)

run(427, 7072300) | debug('Star 2') | eq(3349098263)
