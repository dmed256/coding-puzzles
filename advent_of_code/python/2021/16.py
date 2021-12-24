from repo_utils import *

input_lines = get_input_lines()

class SmartString:
    def __init__(self, value):
        self.value = value
        self.ptr = 0

    def slice(self, length, binary=False):
        end = self.ptr + length
        if len(self.value) < end:
            return None

        value = self.value[self.ptr:end]
        if binary:
            value = int(value, 2)

        self.ptr = end

        return value

def parse_packet(ss):
    version = ss.slice(3, binary=True)
    type_id = ss.slice(3, binary=True)

    info = {
        'version': version,
        'type_id': type_id,
        'raw_value': None,
        'subpackets': [],
    }

    if type_id == 4:
        raw_value = ''
        while True:
            group = ss.slice(5)
            raw_value += group[1:]
            if group[0] == '0':
                break

        return {
            **info,
            'raw_value': int(raw_value, 2),
        }

    length_type_id = ss.slice(1, binary=True)

    if length_type_id == 0:
        subpacket_length = ss.slice(15, binary=True)
        end = ss.ptr + subpacket_length
        subpackets = []
        while ss.ptr < end:
            subpacket = parse_packet(ss)
            if subpacket is None:
                break
            subpackets.append(subpacket)
    else:
        subpacket_count = ss.slice(11, binary=True)
        subpackets = []
        for _ in range(subpacket_count):
            subpackets.append(parse_packet(ss))

    return {
        **info,
        'subpackets': subpackets,
    }

def calc_packet(packet):
    type_id = packet['type_id']

    subpackets = [
        calc_packet(subpacket)
        for subpacket in packet['subpackets']
    ]

    if type_id == 0:
        return sum(subpackets)
    elif type_id == 1:
        return mult(subpackets)
    elif type_id == 2:
        return min(subpackets)
    elif type_id == 3:
        return max(subpackets)
    elif type_id == 4:
        return packet['raw_value']
    elif type_id == 5:
        return all([
            subpackets[i - 1] > subpackets[i]
            for i in range(1, len(subpackets))
        ])
    elif type_id == 6:
        return all([
            subpackets[i - 1] < subpackets[i]
            for i in range(1, len(subpackets))
        ])
    elif type_id == 7:
        return all([
            subpackets[i - 1] == subpackets[i]
            for i in range(1, len(subpackets))
        ])

def run(problem, lines):
    value = lines[0]

    hex_to_binary = {
        '0': '0000',
        '1': '0001',
        '2': '0010',
        '3': '0011',
        '4': '0100',
        '5': '0101',
        '6': '0110',
        '7': '0111',
        '8': '1000',
        '9': '1001',
        'A': '1010',
        'B': '1011',
        'C': '1100',
        'D': '1101',
        'E': '1110',
        'F': '1111',
    }

    output = ''
    for c in value:
        output += hex_to_binary[c]

    ss = SmartString(output)
    packet = parse_packet(ss)

    if problem == 1:
        ans = 0
        queue = [packet]
        while queue:
            info = queue.pop()
            ans += info['version']
            queue.extend(info['subpackets'])

        return ans

    return calc_packet(packet)

run(1, ['8A004A801A8002F478']) | eq(16)
run(1, ['620080001611562C8802118E34']) | eq(12)
run(1, ['C0015000016115A2E0802F182340']) | eq(23)
run(1, ['A0016C880162017C3686B18A3D4780']) | eq(31)

run(1, input_lines) | debug('Star 1') | eq(960)

run(2, ['C200B40A82']) | eq(3)
run(2, ['04005AC33890']) | eq(54)
run(2, ['880086C3E88112']) | eq(7)
run(2, ['CE00C43D881120']) | eq(9)
run(2, ['D8005AC2A8F0']) | eq(1)
run(2, ['F600BC2D8F']) | eq(0)
run(2, ['9C005AC2F8F0']) | eq(0)
run(2, ['9C0141080250320F1802104A08']) | eq(1)

run(2, input_lines) | debug('Star 2') | eq(12301926782560)
