# modification of alignpixels.py that is optimized to focus wider pixel columns
# new optimization is to process blocks vertically

import progressbar
import math
from colormath.color_diff import delta_e_cie2000
from colormath.color_conversions import convert_color
from colormath.color_objects import sRGBColor, LabColor
from PIL import Image
import urllib.request as urllib2
img = Image.open('mosaic10_142_resized_blurred.png')

IMG_WIDTH = img.width
IMG_HEIGHT = img.height

# number of pixels a column is allowed to vertically shift in one direction
MAX_SHIFT_RANGE = 16
# how much of the image to process ( set to a smaller value )
# normally this process takes about 5 minutes to run for the whole image
# using the default shift range of 4 pixels.
# so you may want to set to a smaller value for experimental changes
MAX_IMAGE_WIDTH_TO_ALIGN = IMG_WIDTH  # Default value: IMG_WIDTH

# create target image (filled with red)
target = Image.new(
    'RGB', (IMG_WIDTH, IMG_HEIGHT + 2 * MAX_SHIFT_RANGE), "red")
pixels = target.load()

CHUNK_SIZE = 18

# convert RGB to LAB


def getColorLAB(pixel):
    r, g, b = pixel


#    r = int(r/10)
 #   g = int(g/10)
  #  b = int(b/10)

    return convert_color(sRGBColor(r/255, g/255, b/255), LabColor)

# supposedly the most accurate way to measure human perceptible color difference


def getColorDifferenceLAB(a, b):
    a_lab = getColorLAB(a)
    b_lab = getColorLAB(b)
    return delta_e_cie2000(a_lab, b_lab)


bar = progressbar.ProgressBar(
    max_value=int(MAX_IMAGE_WIDTH_TO_ALIGN / CHUNK_SIZE), redirect_stdout=True)

BLOCK_H = 32

# sweep through the the pixel columns left to right
for x in range(0, MAX_IMAGE_WIDTH_TO_ALIGN, CHUNK_SIZE):
    bar.update(int(x/CHUNK_SIZE))
    img_column_strip = img.crop((x, 0, x+CHUNK_SIZE, IMG_HEIGHT))
    pixel_column = img_column_strip.convert('RGB').load()
    BEST_SCORE = 99999999999
    if (x == 0):
        target.paste(img_column_strip, (x, MAX_SHIFT_RANGE))
    else:
        #

        for b in range(0, IMG_HEIGHT, BLOCK_H):
            block_pixels = img_column_strip.crop((0, b, 0, BLOCK_H))

            # Find the best y-offset for the pixel strip which yields
            # the smallest color difference ( when compared against the
            # left neighboring pixel column )
            for y in range(0, 2 * MAX_SHIFT_RANGE):
                sum = 0
                num_pairs_compared = 0
                for j in range(b, BLOCK_H):
                    r1, g1, b1 = pixel_column[0, j]
                    r2, g2, b2 = pixels[x-1, y+j]
                    # skip any non-overlapped comparisions ( based on red pixel )
                    if (not(r2 == 255 and g2 == 0 and b2 == 0)):
                        num_pairs_compared = num_pairs_compared + 1
                        diff = getColorDifferenceLAB(
                            (r1, g1, b1), (r2, g2, b2))
                        # SSD approach ( sum of squared differences )
                        sum = sum + diff*diff

                # SSD tends to be biased towards smallest overlap, so correct
                # that by normalizing score to a per-pixel
                sum = sum / num_pairs_compared
                if (sum < BEST_SCORE):
                    BEST_SCORE = sum
                    BEST_Y = y
            y = BEST_Y
            # draw strip at best y-location
            target.paste(img_column_strip, (x, y))

# show output
# target = target.convert("RGBA")
target.save("output.png")
target.show()
