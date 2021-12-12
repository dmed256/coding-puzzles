from repo_utils import *

input_value = get_input()
input_lines = get_input_lines()

def decrypt(name, sector_id):
    return ' '.join(
        ''.join(
            chr(ord('a') + ((ord(c) - ord('a') + sector_id) % 26))
            for c in word
        )
        for word in name.split('-')
    )

def run(problem, lines):
    valid_items = []
    for line in lines:
        name, checksum = line[:-1].split('[')

        *name, sector_id = name.split('-')
        name = '-'.join(name)
        sector_id = int(sector_id)

        counts = defaultdict(int)
        for c in name.replace('-', ''):
            counts[c] += 1

        counts = sorted([
            (-count, c)
            for c, count in counts.items()
        ], reverse=False)
        counts = ''.join(c for _, c in counts)

        if checksum == counts[:len(checksum)]:
            valid_items.append((name, checksum, sector_id))

    if problem == 1:
        return sum(
            sector_id
            for _, _, sector_id in valid_items
        )

    for name, checksum, sector_id in valid_items:
        decrypted_phrase = decrypt(name, sector_id)
        if 'northpole object storage' == decrypted_phrase:
            return sector_id

run(1, [
    'aaaaa-bbb-z-y-x-123[abxyz]',
    'a-b-c-d-e-f-g-h-987[abcde]',
    'not-a-real-room-404[oarel]',
    'totally-real-room-200[decoy]',
]) | eq(1514)

run(1, input_lines) | debug('Star 1') | eq(173787)

run(2, input_lines) | debug('Star 2') | eq(548)
