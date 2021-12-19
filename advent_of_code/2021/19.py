from repo_utils import *

input_lines = get_input_lines()

@functools.cache
def get_combinations():
    combinations = [
        (x, y, z)
        for indices in itertools.combinations([1, 2, 3, -1, -2, -3], 3)
        if sum(abs(x) for x in indices) == 6
        for x, y, z in itertools.permutations(indices)
    ]

    # Clean up indices + signs
    return [
        (
            (abs(x) - 1, 1 if x > 0 else -1),
            (abs(y) - 1, 1 if y > 0 else -1),
            (abs(z) - 1, 1 if z > 0 else -1),
        )
        for x, y, z in combinations
    ]

def align_scanner(scanner1, scanner2):
    for combination2 in get_combinations():
        (xi, xs), (yi, ys), (zi, zs) = combination2

        transformed_scanner2 = [
            (
                xs * coord2[xi],
                ys * coord2[yi],
                zs * coord2[zi],
            )
            for coord2 in scanner2
        ]
        counter = Counter([
            (
                coord1[0] - coord2[0],
                coord1[1] - coord2[1],
                coord1[2] - coord2[2],
            )
            for coord1 in scanner1
            for coord2 in transformed_scanner2
        ])

        offset, count = counter.most_common(1)[0]
        if count < 12:
            continue

        dx, dy, dz = offset
        return [
            (x + dx, y + dy, z + dz)
            for x, y, z in transformed_scanner2
        ], offset

    return None, None

def run(lines):
    scanner = None
    scanners = []
    for line in lines:
        if not line:
            continue

        if 'scanner' in line:
            scanners.append([])
            continue

        scanners[-1].append([
            int(x) for x in line.split(',')
        ])

    scanner_ids = set(range(len(scanners)))

    aligned = {0}
    cache = set()
    positions = [(0, 0, 0)]
    while len(aligned) < len(scanners):
        for s1 in set(aligned):
            for s2 in scanner_ids - set(aligned):
                if (s1, s2) in cache:
                    continue
                cache.add((s1, s2))

                # Only transform s2 if s1 is aligned with scanner 0
                if s1 not in aligned:
                    continue

                # No need to re-align s2
                if s2 in aligned:
                    continue

                scanner1 = scanners[s1]
                scanner2 = scanners[s2]

                aligned_scanner2, offset = align_scanner(scanner1, scanner2)

                if aligned_scanner2 is not None:
                    aligned.add(s2)
                    scanners[s2] = aligned_scanner2
                    positions.append(offset)

    beacon_count = len({
        tuple(coord)
        for scanner in scanners
        for coord in scanner
    })

    max_distance = max(
        sum(abs(v1 - v2) for v1, v2 in zip(p1, p2))
        for p1, p2 in itertools.combinations(positions, 2)
    )

    return beacon_count, max_distance

example1 = multiline_lines(r"""
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
""")

run(example1) | eq((79, 3621))

run(input_lines) | debug('Star 1 + 2') | eq((432,14414))
