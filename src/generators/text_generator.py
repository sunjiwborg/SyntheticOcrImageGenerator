import random
import glob
import os
from PIL import Image, ImageFont, ImageDraw

def get_text_layer(text, args):
    font = get_font(args.f, args.s)

    # Measure text
    temp_draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    bbox = temp_draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # Render text layer
    text_layer = Image.new("RGBA", (tw + 10, th + 10), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(text_layer)
    tdraw.text((-bbox[0] + 5, -bbox[1] + 5), text, font=font, fill=get_color(args.tc)) 
    return text_layer

def get_font(path, sizes):
    # Determine font size
    font_size = random.choice(sizes)

    # Find available font
    font_files = glob.glob(os.path.join(path, "*.[to]tf"))
    if font_files:
        font_file = random.choice(font_files)
    else:
        print("Couldn't find fonts")
        exit()
    
    try:
        return ImageFont.truetype(font_file, size=font_size, layout_engine=ImageFont.Layout.RAQM)
    except Exception:
        return ImageFont.load_default(size=font_size)
    
def get_color(colors):
    if isinstance(colors, str):
        colors = colors.split(",")
    return random.choice(colors).strip()
