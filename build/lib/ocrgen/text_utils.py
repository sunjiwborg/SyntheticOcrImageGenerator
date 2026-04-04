import os
import glob
import random
from PIL import ImageFont

def load_dictionary(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def get_font(args):
    font_path = args.font
    if args.font_dir:
        font_files = glob.glob(os.path.join(args.font_dir, "*.[to]tf"))
        if font_files:
            font_path = random.choice(font_files)
    
    try:
        # libraqm is activated via the layout_engine parameter
        return ImageFont.truetype(font_path, size=32, layout_engine=ImageFont.Layout.RAQM)
    except Exception:
        return ImageFont.load_default()