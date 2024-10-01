#!/usr/bin/env python3

import warnings
import sys
import textwrap

with warnings.catch_warnings():
    warnings.simplefilter("ignore")

from PIL import Image, ImageDraw, ImageFont
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster

fontSizeDict = {
    7:75,
    8:60,
    9:60,
    10:50,
    11:43,
    12:43,
    13:37,
    14:37,
    15:33,
    16:30,
    17:30,
    18:27,
    19:27,
    20:25,
    21:23,
    22:23,
    23:21,
    24:21,
    25:20,
    26:19,
    27:19,
    28:17,
    29:17,
    30:17,
    31:16,
    32:16,
    33:15,
    34:14,
    35:14,
    36:14,
    37:13,
    38:13,
    39:13,
    40:12,
    41:12,
    42:12,
    43:11,
    44:11,
    45:11,
    46:11,
    47:10,
    48:10,
    49:10,
    50:10,
}

import textwrap

import sys
print(sys.argv)
def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

def resize_image_keep_aspect_ratio(im, base_width, base_height):
    # Calculate aspect ratio
    original_width, original_height = im.size
    aspect_ratio = original_width / original_height

    # Compute new dimensions based on aspect ratio
    new_width = min(base_width, int(base_height * aspect_ratio))
    new_height = min(base_height, int(base_width / aspect_ratio))

    return im.resize((new_width, new_height), Image.ANTIALIAS)

def textLabel(text,fontsize):

    wrapper = textwrap.TextWrapper(width=fontSizeDict[fontsize])
    text_new=""
    lines = text.splitlines()
    print(lines)


    for l in lines:
        word_list = wrapper.wrap(text=l)

        for ii in word_list[:-1]:
            text_new = text_new + ii + '\n'
        if word_list != []:
            text_new += word_list[-1] + '\n'
    #   Draw print file   #
    print(text_new)
    fnt = ImageFont.truetype('/Library/Fonts/Microsoft/Andale Mono', fontsize)
    width = fnt.getlength(text_new)[0]
    height = fnt.getlength(text_new)[1]
    size = height * (text_new.count('\n') + 1)
    im = Image.new('L', (300, size), color = 'white')
    g = ImageDraw.Draw(im)
    g.text((0,0), text_new , fill='black', font=fnt)
    return im

def printLabel(label_images):
    backend = 'network'
    model = 'QL-700'
    printer = '192.168.1.185'

    qlr = BrotherQLRaster(model)
    qlr.exception_on_warning = False

    instructions = convert(
        qlr=qlr,
        images=label_images,
        label='62',  # Keep this as '62'
        rotate='0',
        threshold=70.0,
        dither=False,
        compress=False,
        dpi_600=False,
        hq=True,
        cut=True
    )

    send(instructions=instructions, printer_identifier=printer, backend_identifier=backend, blocking=True)

def main(mode = "text", path = None, text = None, fontsize = 10):
    label_images = []
    if mode == "text":
        label_images.append(textLabel(text,fontsize))
        printLabel(label_images)
    elif mode == "image":
        im = Image.open(path)

        # Convert 62mm x 25mm to pixels. Assuming 300 DPI:
        # 62mm = 720 pixels, 25mm = 295 pixels
        base_width = 720
        base_height = 295

        im_resized = resize_image_keep_aspect_ratio(im, base_width, base_height)
        
        label_images.append(im_resized)
        printLabel(label_images)
    elif mode == "both":
        try:
            fontsize = int(sys.argv[3])
        except:
            fontsize=10
        label_images.append(textLabel(text,fontsize))
        im = Image.open(path)
        width, height = im.size
        newwidth = int((62/25)*height)
        add = int((newwidth-width)/2)
        im = add_margin(im, 0, add, 0, add, (255, 255, 255))
        label_images.append(im)
        printLabel(label_images)
    else:
        print("Invalid mode! The first arguement must be text, image or both")
  
if __name__ == "__main__":
    main(text="Asmedia", fontsize=14)