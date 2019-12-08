# Day 8: Space Image Format

from utils import *


def decode_image(text, width, height):
    size = width * height
    layers = len(text) // size

    # Find the checksum
    layer_data = [[text[p + i * size] for p in range(size)] for i in range(layers)]
    min_layer = min([(layer_data[i].count('0'), i) for i in range(layers)], key=lambda p: p[0])[0]
    checksum = layer_data[min_layer].count('1') * layer_data[min_layer].count('2')

    # Decode the output image
    output_image = ''
    for p in range(size):
        for i in range(layers):
            if text[p + i * size] != '2':
                output_image += text[p + i * size]
                break
    return output_image, checksum


def print_image(image, width, height):
    print('\n'.join(''.join({'0': '.', '1': '#'}[image[x + (y * width)]] for x in range(width)) for y in range(height)))


if __name__ == '__main__':
    assert decode_image('0222112222120000', 2, 2) == ('0110', 0)

    puzzle_input, puzzle_width, puzzle_height = get_input(), 25, 6
    decoded_image, puzzle_checksum = decode_image(get_input(), puzzle_width, puzzle_height)

    print('Part 1:', puzzle_checksum)
    print('Part 2:')
    print_image(decoded_image, puzzle_width, puzzle_height)
