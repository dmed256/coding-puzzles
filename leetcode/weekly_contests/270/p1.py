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
