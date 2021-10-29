# Wrong: 41920054595687
# Wrong: 68160128016288
# Wrong: 112798141866005
# Wrong: 36455596558889
# Wrong: 98178534353069
# Wrong: 69620352108419
# Wrong: 12741645857315
# 96797432275571

def get_coefficients(lines, deck_size):
    mult = 1
    shift = 0

    for line in lines:
        line = line.strip()
        if line.startswith('deal with increment '):
            value = int(line.split('deal with increment ')[1])
            mult = (mult * value) % deck_size
            shift = (shift * value) % deck_size
        elif line.startswith('cut '):
            value = int(line.split('cut ')[1])
            shift = (shift - value + deck_size) % deck_size
        elif line == 'deal into new stack':
            m = deck_size - 1
            mult = (mult * m) % deck_size
            shift = ((shift + 1) * m) % deck_size

    return [mult, shift]

def get_apply_coefficients(mult, shift, deck_size, applications):
    base2_mult = mult
    base2_mults = [mult]
    base2_shift = 1
    base2_shifts = [1]

    for i in range(100):
        base2_shift = (base2_shift + (base2_shift * base2_mult)) % deck_size
        base2_shifts.append(base2_shift)
        base2_mult = (base2_mult * base2_mult) % deck_size
        base2_mults.append(base2_mult)

    def get_shift_coeff(value):
        coeff = 1
        for i in range(100):
            base2 = 1 << i
            if value & base2:
                coeff = (coeff * base2_mults[i]) % deck_size
        return coeff

    apply_mult = 1
    apply_shift = 0
    shift_position = 0
    for i in range(100):
        base2 = 1 << i
        if applications & base2:
            apply_mult = (apply_mult * base2_mults[i]) % deck_size

            apply_shift_coeff = get_shift_coeff(shift_position)
            apply_shift = (apply_shift + (apply_shift_coeff * base2_shifts[i])) % deck_size
            shift_position += base2

    apply_shift = (shift * apply_shift) % deck_size

    return [apply_mult, apply_shift]


def run_apply(pos, mult, shift, deck_size):
    return ((pos * mult) + shift) % deck_size

def test_application(test_name, input_value, expected_output):
    print(f"RUNNING: {test_name}")
    deck_size = len(expected_output)

    [mult, shift] = get_coefficients(
        input_value.strip().splitlines(),
        deck_size,
    )

    output = list(range(deck_size))
    for i in range(deck_size):
        output[run_apply(i, mult, shift, deck_size)] = i

    if expected_output != output:
        print(f"FAILED: {test_name}")
        print(f"  - Expected: {expected_output}")
        print(f"  - Received: {output}")

def test_applications(test_name, mult, shift, expected_output, applications):
    print(f"RUNNING: {test_name}")

    output = get_apply_coefficients(mult, shift, 1000000000000, applications)

    if expected_output != output:
        print(f"FAILED: {test_name}")
        print(f"  - Expected: {expected_output}")
        print(f"  - Received: {output}")

test_application("tutorial1", """
deal into new stack
""", [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
)

test_application("tutorial2", """
cut 3
""", [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]
)

test_application("tutorial3", """
cut -4
""", [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]
)

test_application("tutorial4", """
deal with increment 3
""", [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]
)

test_application("test1", """
deal with increment 7
deal into new stack
deal into new stack
""", [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]
)

test_application("test2", """
cut 6
deal with increment 7
deal into new stack
""", [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]
)

test_application("test3", """
deal with increment 7
deal with increment 9
cut -2
""", [6, 3, 0, 7, 4, 1, 8, 5, 2, 9]
)

test_application("test4", """
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
""", [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]
)

test_applications(
    "applications - test1",
    2, 1,
    [2, 1],
    1,
)
test_applications(
    "applications - test2",
    2, 1,
    [4, 3],
    2,
)
test_applications(
    "applications - test3",
    2, 1,
    [8, 7],
    3,
)
test_applications(
    "applications - test4",
    2, 1,
    [16, 15],
    4,
)
test_applications(
    "applications - test5",
    1, 1,
    [1, 10000],
    10000,
)
test_applications(
    "applications - test6",
    7, 0,
    [7*7*7*7, 0],
    4,
)

#---[ Star 1 ]--------------------------
with open('input', 'r') as fd:
    lines = fd.readlines()

deck_size = 10007

[mult, shift] = get_coefficients(lines, deck_size)
assert 4284 == run_apply(2019, mult, shift, deck_size)

#---[ Star 2 ]--------------------------
deck_size = 119315717514047
applications = 101741582076661

for i in range(20):
    mult = 382930490
    shift = 729083420
    x = 112798141866005

    expected_value = x
    for j in range(i):
        expected_value = ((mult * expected_value) + shift) % deck_size

    [mult, shift] = get_apply_coefficients(mult, shift, deck_size, i)
    value = ((mult * x) + shift) % deck_size
    if value != expected_value:
        print(f"FAILED({i}):")
        print(f"  - Expected: {expected_value}")
        print(f"  - Received: {value}")


[mult, shift] = get_coefficients(lines, deck_size)

[mult, shift] = get_apply_coefficients(mult, shift, deck_size, applications)
print(f"{mult} * x + {shift} = 2020 (mod {deck_size})")

answer = int(input("Input answer: "))
assert 2020 == run_apply(answer, mult, shift, deck_size)
