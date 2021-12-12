class Solution:
    def countPoints(self, rings: str) -> int:
        rods = [set() for _ in range(10)]
        for i in range(0, len(rings), 2):
            color = rings[i]
            rod = int(rings[i + 1])
            rods[rod].add(color)

        return len([
            1
            for i, rod in enumerate(rods)
            if len(rod) == 3
        ])
