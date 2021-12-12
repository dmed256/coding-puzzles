from repo_utils import *

import bisect

class Solution:
    def maxTotalFruits(self, fruits, start_pos, max_steps):
        positions = [pos for pos, amt in fruits]
        amounts = [amt for pos, amt in fruits]

        # TODO


fruits = [[1,4],[3,7],[4,8],[6,5],[10,3],[12,8],[13,6],[14,5],[16,3],[18,7],[22,7],[24,1],[28,7],[32,3],[34,7],[35,7],[37,7],[40,7]]
Solution().maxTotalFruits(fruits, 41, 10) | eq(31)

fruits = [[200000,10000]]
Solution().maxTotalFruits(fruits, 200000, 0) | eq(10000)

fruits = [[200000,10000]]
Solution().maxTotalFruits(fruits, 0, 0) | eq(0)

fruits = [[0,10],[1,6],[2,4],[8,10],[9,5],[13,3],[14,3],[23,4],[28,5],[29,7],[30,6],[32,2],[33,8],[36,4],[40,9]]
Solution().maxTotalFruits(fruits, 0, 23) | eq(45)
