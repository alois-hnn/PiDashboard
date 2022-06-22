from luma.core.interface.serial import i2c
from luma.core.interface.parallel import bitbang_6800   # purpose?
from luma.core.render import canvas
from luma.oled.device import ssd1306

import time
import psutil
from PIL import Image, ImageOps, ImageDraw, ImageFont

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)
width = device.size[0]
height = device.size[1]

def getBarWidth():
    percentage = psutil.cpu_percent()
    return width * (percentage / 100)

def createBar():
    bar = Image.new("RGB", (128, 30))
    barDraw = ImageDraw.Draw(bar)
    barDraw.rectangle([0, 0, 127, 25], fill=None, outline="white", width=1)
    barDraw.rectangle([0, 0, getBarWidth(), 25], fill="white", outline="white", width=1)
    return bar

def createPicture():
    image = Image.open('cpu.png').convert("RGBA")

    if image.mode == 'RGBA':
        r, g, b, a = image.split()
        rgb_image = Image.merge('RGB', (r,g,b))

        inverted_image = ImageOps.invert(rgb_image)

        r2,g2,b2 = inverted_image.split()

        final_transparent_image = Image.merge('RGBA', (r2,g2,b2,a)).resize((30, 30))
    else:
        final_transparent_image = PIL.ImageOps.invert(image)

    return final_transparent_image

def createCaption():
    caption = Image.new("RGB", (98,30), "black")
    captionDraw = ImageDraw.Draw(caption)
    # captionDraw.text((20, 7), "CPU Usage")
    
    # use for custom fonts

    # fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 14)
    fnt = ImageFont.truetype("fonts/code2000.ttf", 14)
    captionDraw.text((12, 6), "CPU Usage", font=fnt, fill=(255,255,255))

    return caption

def updateBackground(image, caption, bar):
    background = Image.new("RGBA", device.size, (0, 0, 0, 0))
    background.paste(image, (0, 0)) # position param
    background.paste(caption, (30, 0))
    background.paste(bar, (0, height-26))
    device.display(background.convert(device.mode))

def trash():

    barWidth = getBarWidth()

    with canvas(device) as draw:

        # raw.text((40, 10), "CPU Usage", fill="white")
        
        draw.rectangle((0, 35) + (width - 1, height -1), "black", "white")
        draw.rectangle((0, 35) + (barWidth, height -1), "white", "white")


if __name__ == "__main__":
    try:
        image = createPicture()
        caption = createCaption()
        while True:
            bar = createBar()
            updateBackground(image, caption, bar) 
            
    except KeyboardInterrupt:
        print("Application interrupted by user")