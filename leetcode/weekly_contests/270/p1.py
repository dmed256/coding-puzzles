from repo_utils import *

import itertools

class Solution:
    def findEvenNumbers(self, inputs):
        numbers = set()
        for comb in itertools.combinations(inputs, 3):
            for digits in itertools.permutations(comb):
                if digits[0] == 0 or digits[2] % 2:
                    continue
                numbers.add(digits[0] * 100 + digits[1] * 10 + digits[2])

        return sorted(list(numbers))

def run(inputs):
    return Solution().findEvenNumbers(inputs)

run([2,1,3,0]) | eq([102,120,130,132,210,230,302,310,312,320])
run([2,2,8,8,2]) | eq([222,228,282,288,822,828,882])
run([3,7,5]) | eq([])
run([0,2,0,0]) | eq([200])
run([0,0,0]) | eq([])
