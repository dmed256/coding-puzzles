from advent_of_code import *
from int_processor import *

input_value = get_input()

packets = {0: []}

def packet_count():
    return sum(len(v) for v in packets.values())

class Network:
    def __init__(self, address):
        self.address = address

        self.p = IntProcessor(input_value)
        self.p.get_input = self.get_input
        self.p.process_output = self.process_output

        self.initialized = False
        self.tried_empty = False
        self.is_idle = False

    def get_input_value(self):
        if not self.initialized:
            self.initialized = True
            return self.address

        values = packets.get(self.address, [])
        if values:
            self.is_idle = False
            # print(f'1. [{self.address}] -> values = {values}')
            return values.pop(0)

        if not packet_count() and not self.tried_empty:
            self.tried_empty = True
            self.is_idle = True
            return -1

        # print(f'input[{self.address}] -> {packets} ({packet_count()})')
        self.tried_empty = False
        self.is_idle = True
        return PAUSE

    def get_input(self):
        return self.get_input_value()

    def process_output(self, output):
        if len(output) < 3:
            return output
        [address, x, y] = output

        values = packets.get(address, [])
        values.append(x)
        values.append(y)
        packets[address] = values
        # print(f'output[{self.address}] -> {packets}({packet_count()})')

        return []

    def run(self):
        if not self.initialized:
            self.p.run()
        else:
            self.unpause()

    def unpause(self):
        value = self.get_input_value()
        if value != PAUSE:
            self.p.unpause(value)

networks = [
    Network(i)
    for i in range(50)
]

def network_is_idle():
    return 255 in packets and (
        50 == sum(
            n.is_idle
            for n in networks
        )
    )

def run_networks():
    while not network_is_idle():
        for i in range(50):
            networks[i].run()

    nat_packets = packets[255]
    del packets[255]

    [x, y] = nat_packets[-2:]

    packets[0].append(x)
    packets[0].append(y)

    return y


y = run_networks() | debug('Star 1')

prev_y = y
while True:
    y = run_networks()
    if prev_y == y:
        break
    prev_y = y

y | debug('Star 2')
