from repo_utils import *

def run(problem, value, disk_size):
    while len(value) <= disk_size:
        value2 = value[::-1]
        value2 = value2.replace('1', '2')
        value2 = value2.replace('0', '1')
        value2 = value2.replace('2', '0')
        value += '0'
        value += value2

    value = value[:disk_size]

    while True:
        checksum = ''
        for i in range(0, len(value), 2):
            if value[i] == value[i + 1]:
                checksum += '1'
            else:
                checksum += '0'
        if len(checksum) % 2:
            break

        value = checksum

    return checksum

run(1, '110010110100', 12) | eq('100')

run(1, '10000', 20) | eq('01100')

run(1, '00101000101111010', 272) | debug('Star 1') | eq('10010100110011100')

run(1, '00101000101111010', 35651584) | debug('Star 2') | eq('01100100101101100')
