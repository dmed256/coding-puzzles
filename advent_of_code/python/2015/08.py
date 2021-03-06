import re
from repo_utils import *

def line_string_size(line):
    return len(line)

def line_byte_size(line):
    line = line[1:-1]

    pattern = r'(\\(?:x..|"|\\))'
    words = re.split(pattern, line)
    return sum([
        len(word) if re.fullmatch(pattern, word) is None else 1
        for word in words
    ])

def line_encode_size(line):
    line = line.replace('\\', '\\\\')
    line = line.replace('"', '\\"')
    return len(line) + 2

def string_size(lines):
    return sum(
        line_string_size(line.strip())
        for line in lines
    )

def byte_size(lines):
    return sum(
        line_byte_size(line.strip())
        for line in lines
    )

def encode_size(lines):
    return sum(
        line_encode_size(line.strip())
        for line in lines
    )

def run(lines):
    return string_size(lines) - byte_size(lines)

def run2(lines):
    return encode_size(lines) - string_size(lines)

example = multiline_lines(r"""
""
"abc"
"aaa\"aaa"
"\x27"
""")

string_size(example) | eq(23)
byte_size(example) | eq(11)
run(example) | eq(12)

input_lines = get_input_lines()

run(input_lines) | debug('Star 1')

line_encode_size(r'""') | eq(6)
line_encode_size(r'"abc"') | eq(9)
line_encode_size(r'"aaa\"aaa"') | eq(16)
line_encode_size(r'"\x27"') | eq(11)

run2(input_lines) | debug('Star 2')
