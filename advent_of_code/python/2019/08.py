import re
from repo_utils import *

def get_digit_count(layer):
    count = {
        i: 0
        for i in range(10)
    }
    for c in layer:
        count[int(c)] += 1
    return count

def get_layers(lines, width, height):
    pixels = width * height
    return [
        [
            int(pixel)
            for pixel in lines[i*pixels:(i + 1)*pixels]
        ]
        for i in range(len(lines) // pixels)
    ]

def print_layer(layer, width):
    output = ''
    for i, pixel in enumerate(layer):
        if i and not (i % width):
            output += '\n'
        if pixel:
            output += '■'
        else:
            output += ' '

    print(output)

def print_image(layers, width, height):
    pixels = width * height
    image = [0 for i in range(pixels)]
    finished_pixels = set()
    for layer in layers:
        if len(finished_pixels) == pixels:
            break

        for i, pixel in enumerate(layer):
            if i not in finished_pixels and pixel != 2:
                image[i] = pixel
                finished_pixels.add(i)

    print_layer(image, width)

def run(lines, width, height):
    layers = get_layers(lines, width, height)
    print_image(layers, width, height)
    digit_count = [
        get_digit_count(layer)
        for layer in layers
    ]
    min_counts = min(digit_count, key=lambda x: x[0])
    return min_counts[1] * min_counts[2]

example1 = '123456789012'
example2 = '0222112222120000'

run(example1, 3, 2) | eq(1)
run(example2, 2, 2)

input_value = get_input()

print('\n\nProblem ->')
run(input_value, 25, 6) | debug('Star 1') | eq(2975)
