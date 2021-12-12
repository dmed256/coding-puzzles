class Solution:
    def minimumRefill(self, plants: List[int], capacityA: int, capacityB: int) -> int:
        refills = 0

        bucket1 = capacityA
        bucket2 = capacityB
        ptr1 = 0
        ptr2 = len(plants) - 1

        while ptr1 <= ptr2:
            v1 = plants[ptr1]
            v2 = plants[ptr2]

            if bucket1 < v1:
                refills += 1
                bucket1 = capacityA - v1
            else:
                bucket1 -= v1

            if bucket2 < v2:
                refills += 1
                bucket2 = capacityB - v2
            else:
                bucket -= v2

            ptr1 += 1
            ptr2 -= 1

            if ptr1 == ptr2:
                v = plants[ptr1]
                if max(bucket1, bucket2) < v:
                    refills += 1
                break

        return refills
