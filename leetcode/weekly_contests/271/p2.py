class Solution:
    def subArrayRanges(self, nums):
        ans = 0

        for i in range(len(nums)):
            min_value = nums[i]
            max_value = nums[i]
            for j in range(i, len(nums)):
                min_value = min(min_value, nums[j])
                max_value = max(max_value, nums[j])

                ans += max_value - min_value

        return ans
