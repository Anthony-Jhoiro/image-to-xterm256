import sys
from PIL import Image
import os

from color import rgb2short

FONT_RATIO = 0.43
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



def print_tile(tile: Image):
    """
   Given PIL Image, return average value of grayscale value
   """
    # get image as numpy array
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

    print("\u001b[38;5;" + str(color) + "m" + char, end="")
    # exit(0)





def get_terminal_sizes():
    columns, lines = os.get_terminal_size()
    return lines, columns, columns * lines



def main():
    if len(sys.argv) != 2:
        print("Missing filename")
        exit(1)
    file_name = sys.argv[1]

    image = Image.open(file_name).convert('RGB')

    image_width, image_height = image.size

    image_ratio = image_width / image_height

    terminal_height, terminal_width, terminal_ratio = get_terminal_sizes()

    max_tile_width = image_width // terminal_width
    max_tile_height = image_height // terminal_height

    if max_tile_width > max_tile_height:
        tile_height = max_tile_height
        tile_width = max_tile_height * FONT_RATIO
        vertical_margin = 0
    else:
        tile_width = max_tile_width
        tile_height = max_tile_width / FONT_RATIO
        vertical_margin = terminal_height - (tile_height / 8)

    for row in range(terminal_height):
        y1 = row * tile_height

        if row == terminal_height - 1:
            y2 = image_height
        else:
            y2 = (row + 1) * tile_height

        for col in range(terminal_width):
            x1 = col * tile_width

            if col == terminal_width - 1:
                x2 = image_width
            else:
                x2 = (col + 1) * tile_width

            tile = image.crop((x1, y1, x2, y2))

            print_tile(tile)

        print("")


if __name__ == '__main__':
    main()
