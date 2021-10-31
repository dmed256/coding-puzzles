import re
import itertools
from termcolor import colored
from advent_of_code import *
from int_processor import *

def get_signal(
        values,
        loop_mode,
        phase_settings,
):
    amplifier_processors = [
        IntProcessor(values, loop_mode)
        for i in range(5)
    ]
    p_inputs = [
        [phase_setting]
        for phase_setting in phase_settings
    ]

    is_done = False
    signal = 0
    last_output = 0
    while not is_done:
        for amp in range(5):
            processor = amplifier_processors[amp]
            if processor.is_done:
                continue

            inputs = [*p_inputs[amp], last_output]

            outputs = processor.run(inputs=inputs)
            if outputs:
                last_output = outputs[-1]
                # Get the output from the last amplifier
                if amp == 4:
                    signal = last_output

            p_inputs[amp] = []

            if processor.is_done:
                is_done = amp == 4
                continue

            if outputs is None:
                processor.print_debug()
                raise 1
                break

    return signal

def run(values, loop_mode, phase_setting_sequence):
    values = split_comma_ints(values)

    max_signal = 0
    for phase_settings in itertools.permutations(phase_setting_sequence):
        signal = get_signal(
            values,
            loop_mode,
            phase_settings,
        )
        if signal is not None:
            max_signal = max(max_signal, signal)

    return max_signal

example1 = multiline_input(r"""
3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0
""")
example2 = multiline_input(r"""
3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0
""")
example3 = multiline_input(r"""
3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0
""")

run(
    example1,
    SINGLE_LOOP_MODE,
    [0, 1, 2, 3, 4],
) | eq(43210)

run(
    example2,
    SINGLE_LOOP_MODE,
    [0, 1, 2, 3, 4],
) | eq(54321)

run(
    example3,
    SINGLE_LOOP_MODE,
    [0, 1, 2, 3, 4],
) | eq(65210)

input_value = get_input()

run(
    input_value,
    SINGLE_LOOP_MODE,
    [0, 1, 2, 3, 4],
) | debug('Star 1')

example1 = multiline_input("""
3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
""")
example2 = multiline_input("""
3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10
""")

run(
    example1,
    FEEDBACK_LOOP_MODE,
    [5, 6, 7, 8, 9],
) | eq(139629729)

run(
    example2,
    FEEDBACK_LOOP_MODE,
    [5, 6, 7, 8, 9],
) | eq(18216)

run(
    input_value,
    FEEDBACK_LOOP_MODE,
    [5, 6, 7, 8, 9],
) | debug('Star 2')