import math
from sympy import symbols
from sympy.solvers.diophantine import diophantine
from repo_utils import *


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


def run(input_lines, deck_size, pos):
    [mult, shift] = get_coefficients(input_lines, deck_size)
    return run_apply(pos, mult, shift, deck_size)


def run2(input_lines, deck_size, applications, pos):
    [mult, shift] = get_coefficients(input_lines, deck_size)
    [mult, shift] = get_apply_coefficients(mult, shift, deck_size, applications)
    #    mult * x + shift = 2020 (mod deck_size)
    # -> mult * x + shift = 2020 + y * deck_size
    # -> mult * x + deck_size * y + (shift - 2020) = 0

    x, y, t = symbols("x, y, t_0", integer=True)
    (sx, sy) = list(
        diophantine(mult*x - deck_size*y + (shift - 2020))
    )[0]

    # ax + b = 0
    (x_b, x_ax) = sx.as_coeff_Add()
    (x_a, _) = x_ax.as_coeff_Mul()

    answer = sx.subs({
        t: math.ceil(-x_b / x_a)
    })

    run_apply(answer, mult, shift, deck_size) | eq(pos)

    return answer


def run_test(deck_size, input_lines):
    output = [0] * deck_size
    for i in range(deck_size):
        output[run(input_lines, deck_size, i)] = i
    return output


example1 = multiline_lines("""
deal into new stack
""")

example2 = multiline_lines("""
cut 3
""")

example3 = multiline_lines("""
cut -4
""")

example4 = multiline_lines("""
deal with increment 3
""")

example5 = multiline_lines("""
deal with increment 7
deal into new stack
deal into new stack
""")

example6 = multiline_lines("""
cut 6
deal with increment 7
deal into new stack
""")

example7 = multiline_lines("""
deal with increment 7
deal with increment 9
cut -2
""")

example8 = multiline_lines("""
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
""")

run_test(10, example1) | eq([9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
run_test(10, example2) | eq([3, 4, 5, 6, 7, 8, 9, 0, 1, 2])
run_test(10, example3) | eq([6, 7, 8, 9, 0, 1, 2, 3, 4, 5])
run_test(10, example4) | eq([0, 7, 4, 1, 8, 5, 2, 9, 6, 3])
run_test(10, example5) | eq([0, 3, 6, 9, 2, 5, 8, 1, 4, 7])
run_test(10, example6) | eq([3, 0, 7, 4, 1, 8, 5, 2, 9, 6])
run_test(10, example7) | eq([6, 3, 0, 7, 4, 1, 8, 5, 2, 9])
run_test(10, example8) | eq([9, 2, 5, 8, 1, 4, 7, 0, 3, 6])

input_lines = get_input_lines()
run(input_lines, 10007, 2019) | debug('Star 1') | eq(4284)

# Test get_apply_coefficients
mult = 382930490
shift = 729083420
x = 112798141866005
deck_size = 119315717514047
for i in range(20):
    expected_value = x
    for j in range(i):
        expected_value = ((mult * expected_value) + shift) % deck_size

    [mult, shift] = get_apply_coefficients(mult, shift, deck_size, i)
    value = ((mult * x) + shift) % deck_size
    value | eq(expected_value)

run2(
    input_lines,
    deck_size,
    applications=101741582076661,
    pos=2020,
) | debug('Star 2') | eq(96797432275571)
