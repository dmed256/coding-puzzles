import hashlib
from advent_of_code import *

def md5(s):
    return hashlib.md5(str.encode(s)).hexdigest()

def run(s, hash_prefix):
    suffix = 0
    while not md5(f'{s}{suffix}').startswith(hash_prefix):
        suffix += 1
    return suffix

run('abcdef', '00000') | eq(609043)
run('pqrstuv', '00000') | eq(1048970)

run('iwrupvqb', '00000') | debug('Star 1')

run('iwrupvqb', '000000') | debug('Star 2')
