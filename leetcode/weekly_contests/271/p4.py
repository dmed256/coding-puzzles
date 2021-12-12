import bisect

class Solution:
    def maxTotalFruits(self, fruits, start_pos, max_steps):
        positions = [pos for pos, amt in fruits]

        start_score = 0
        # If we start in a fruit, pick it to avoid dealing with conflicting indices
        if start_pos in positions:
            idx = bisect.bisect_left(positions, start_pos)
            positions.pop(idx)
            pos, amt = fruits.pop(idx)
            start_score = amt

        # Empty case
        if not fruits:
            return start_score

        # Find fruits left and right of the start_pos
        if start_pos < positions[0]:
            left = []
            right = fruits
        elif positions[-1] < start_pos:
            left = fruits
            right = []
        else:
            right_idx = bisect.bisect(positions, start_pos)
            left = fruits[:right_idx]
            right = fruits[right_idx:]

        left = [
            (start_dist, amt)
            for pos, amt in left
            if (start_dist := abs(pos - start_pos)) is not None
            if start_dist <= max_steps
        ]
        right = [
            (start_dist, amt)
            for pos, amt in right
            if (start_dist := abs(pos - start_pos)) is not None
            if start_dist <= max_steps
        ]

        # Sum the amounts
        for i in range(len(left) - 2, -1, -1):
            left[i] = (left[i][0], left[i][1] + left[i + 1][1])

        for i in range(1, len(right)):
            right[i] = (right[i][0], right[i][1] + right[i - 1][1])

        print(left, right)

        # Check base cases
        if not left and not right:
            return start_score

        if not left:
            return start_score + right[-1][1]

        if not right:
            return start_score + left[0][1]

        # We need to check all sub-ranges
        max_score = max(left[0][1], right[-1][1])

        left_ptr = 0
        right_ptr = 0
        while True:
            left_start_dist, left_amt = left[left_ptr]
            right_start_dist, right_amt = right[right_ptr]

            min_dist = min(left_start_dist, right_start_dist)
            max_dist = max(left_start_dist, right_start_dist)
            steps_left = max_steps - (2 * min_dist) - max_dist
            if 0 <= steps_left:
                max_score = max(max_score, left_amt + right_amt)
                right_ptr += 1
            else:
                left_ptr += 1

            if left_ptr == len(left) or right_ptr == len(right):
                break

        return max_score + start_score
