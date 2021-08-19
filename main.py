import sys
from PIL import Image
import os
import math


FONT_RATIO = 0.4
ASCII_SCALE = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
ASCII_SCALE_SIZE = len(ASCII_SCALE)

COLORS_STEPS = [
    (0, 95),
    (95, 135),
    (135, 175),
    (175, 215),
    (215, 255)
]


def round_tint(tint: int):
    m = 0
    for step_low, step_max in COLORS_STEPS:
        if step_low <= tint <= step_max:
            return m if abs(tint - step_low) < abs(tint - step_max) else m + 1
        m += 1
    return 0


def get_xterm_color(r, g, b):
    rr = round_tint(r)
    rg = round_tint(g)
    rb = round_tint(b)

    return 16 + rr * 36 + rg * 6 + rb


def get_char_from_light(light: int):
    index = int((light * (ASCII_SCALE_SIZE - 1)) / 255)
    return ASCII_SCALE[index]


def print_tile(tile: Image.Image):
    """
    Given PIL Image, return average value of grayscale value
    """
    width, height = tile.size

    pixels = tile.getcolors(width * height)

    most_frequent_pixel = pixels[0]

    for count, color in pixels:
        if count > most_frequent_pixel[0]:
            most_frequent_pixel = (count, color)

    r, g, b = most_frequent_pixel[1]

    light = r * 299/1000 + g * 587/1000 + b * 114/1000

    char = get_char_from_light(light)

    color = get_xterm_color(r, g, b)

    print("\u001b[38;5;" + str(color) + "m" + char, end="\033[0m")
    # print("\u001b[38;5;" + str(color) + "m ", end="")


def get_terminal_sizes():
    columns, lines = os.get_terminal_size()
    return lines, columns, columns / lines


def print_vertical_margin(size: int):
    for i in range(size):
        print("")


def print_top_border(content_width: int):
    print("+", end="")
    for i in range(content_width):
        print("-", end="")
    print("+")


def print_horizontal_margin(size: int):
    for i in range(size):
        print("", end="")


def main():
    if len(sys.argv) != 2:
        print("Missing filename")
        exit(1)
    file_name = sys.argv[1]

    image = Image.open(file_name).convert('RGB')

    image_width, image_height = image.size

    image_ratio = image_width / image_height

    terminal_height, terminal_width, terminal_ratio = get_terminal_sizes()

    grid_height = terminal_height - 2
    grid_width = terminal_width - 2

    if grid_width * FONT_RATIO / image_ratio < grid_height:
        tile_width = math.floor(image_width / grid_width)
        tile_height = math.floor(tile_width / FONT_RATIO / image_ratio)
    else:
        tile_height = math.floor(image_height / grid_height)
        tile_width = int(tile_height * image_ratio)

    image_row_count = math.floor(image_height / tile_height)
    image_col_count = math.floor(image_width / tile_width)

    while image_row_count >= grid_height:
        tile_height += 1
        image_row_count = math.floor(image_height / tile_height)

    while image_col_count >= grid_width:
        tile_width += 1
        image_col_count = math.floor(image_width / tile_width)

    vertical_margin = grid_height - image_row_count
    horizontal_margin = grid_width - image_col_count

    print_vertical_margin(vertical_margin // 2)

    print_horizontal_margin(horizontal_margin // 2)

    print_top_border(image_col_count)

    for row in range(image_row_count):
        y1 = row * tile_height

        if row == image_row_count - 1:
            y2 = image_height
        else:
            y2 = (row + 1) * tile_height

        print_horizontal_margin(horizontal_margin // 2)
        print("|", end="")

        for col in range(image_col_count):
            x1 = col * tile_width

            x2 = image_width if col == image_col_count - 1 else (col + 1) * tile_width

            tile = image.crop((x1, y1, x2, y2))

            print_tile(tile)

        print("|")

    print_horizontal_margin(horizontal_margin // 2)

    print_top_border(image_col_count)

    print_vertical_margin(vertical_margin // 2)


if __name__ == '__main__':
    main()
