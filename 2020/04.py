from advent_of_code import *

input_lines = get_input_lines()

def get_passports(lines):
    passports = [[]]
    for line in lines:
        if line:
            passports[-1].append(line)
        else:
            passports[-1] = ' '.join(passports[-1])
            passports.append([])
    passports[-1] = ' '.join(passports[-1])

    return [
        {
            kv[0]: kv[1]
            for info in p.split(' ')
            if (kv := info.split(':'))
            if kv[1]
        }
        for p in passports
        if p
    ]

def run(lines):
    passports = get_passports(lines)

    required_fields = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])
    return len([
        p
        for p in passports
        if set(p.keys()) >= required_fields
    ])

example1 = multiline_lines(r"""
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
""")

run(example1) | eq(2)
run(input_lines) | debug('Star 1')

def is_valid(p):
    byr = p.get('byr')
    if not byr or not byr.isdigit():
        return False
    if not 1920 <= int(byr) <= 2002:
        return False

    iyr = p.get('iyr')
    if not iyr or not iyr.isdigit():
        return False
    if not 2010 <= int(iyr) <= 2020:
        return False

    eyr = p.get('eyr')
    if not eyr or not eyr.isdigit():
        return False
    if not 2020 <= int(eyr) <= 2030:
        return False

    hgt = p.get('hgt')
    if not hgt or hgt[-2:] not in ['cm', 'in']:
        return False
    hgt_value = int(hgt[:-2])
    if hgt.endswith('cm') and not 150 <= hgt_value <= 193:
        return False
    if hgt.endswith('in') and not 59 <= hgt_value <= 76:
        return False

    hcl = p.get('hcl')
    if not hcl or not hcl.startswith('#') or len(hcl) != 7:
        return False

    ecl = p.get('ecl')
    if ecl not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
        return False

    pid = p.get('pid')
    if not pid or not pid.isdigit() or len(pid) != 9:
        return False

    return True

def run2(lines):
    passports = get_passports(lines)
    return len([
        p
        for p in passports
        if is_valid(p)
    ])

example1 = multiline_lines(r"""
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
""")

example2 = multiline_lines(r"""
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
""")

run2(example1) | eq(0)
run2(example2) | eq(4)
run2(input_lines) | debug('Star 2')
