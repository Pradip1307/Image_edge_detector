#!/usr/bin/env python3

import sys
from PIL import Image

tolerance = 15  # lower tolerance => more noise

def help(exit_code=None):
    print("""usage: {} [options] [input image] [output image]

options:
    -t  --tolerance=[0-100] : tolerance value for edges (default: {})
                              lower values will generate more noise

example:
    python {} -t 5 input.png output.png""".format(sys.argv[0], tolerance, sys.argv[0]))
    sys.exit(exit_code)

def get_avg_pixel(image, x, y):
    r, g, b = image.getpixel((x, y))
    return (r + g + b) // 3

# Process command-line arguments
args = sys.argv[1:]
if len(args) < 2:
    help(2)

if args[0] in ("-h", "--help"):
    help(0)

if args[0] in ("-t", "--tolerance"):
    try:
        tolerance = int(args[1])
    except ValueError:
        help(2)
    args = args[2:]

# Read input image
in_file = args[0]
out_file = args[1] if len(args) > 1 else 'output.png'

try:
    img = Image.open(in_file)
except IOError:
    print("Error: Cannot open input image")
    sys.exit(1)

width, height = img.size
matrix = [[None] * width for _ in range(height)]

# Detect edges
for y in range(1, height - 1):
    for x in range(1, width - 1):
        avg_pixel = get_avg_pixel(img, x, y)
        if (abs(get_avg_pixel(img, x-1, y) - avg_pixel) / 255 * 100 > tolerance or
            abs(get_avg_pixel(img, x+1, y) - avg_pixel) / 255 * 100 > tolerance or
            abs(get_avg_pixel(img, x, y-1) - avg_pixel) / 255 * 100 > tolerance or
            abs(get_avg_pixel(img, x, y+1) - avg_pixel) / 255 * 100 > tolerance or
            abs(get_avg_pixel(img, x-1, y-1) - avg_pixel) / 255 * 100 > tolerance or
            abs(get_avg_pixel(img, x+1, y+1) - avg_pixel) / 255 * 100 > tolerance or
            abs(get_avg_pixel(img, x+1, y-1) - avg_pixel) / 255 * 100 > tolerance or
            abs(get_avg_pixel(img, x-1, y+1) - avg_pixel) / 255 * 100 > tolerance):
            matrix[y][x] = 1

# Remove noise
for y in range(1, height - 1):
    for x in range(1, width - 1):
        if matrix[y][x] is not None:
            if (matrix[y][x+1] is None and
                matrix[y][x-1] is None and
                matrix[y-1][x-1] is None and
                matrix[y-1][x] is None and
                matrix[y-1][x+1] is None and
                matrix[y+1][x-1] is None and
                matrix[y+1][x] is None and
                matrix[y+1][x+1] is None):
                matrix[y][x] = None

# Create new image with
