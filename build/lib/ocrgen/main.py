import argparse
import os
import random
from PIL import Image, ImageDraw
from .text_utils import load_dictionary, get_font
from .image_utils import apply_effects, get_font_color
from .bg_utils import generate_background

def main():
    parser = argparse.ArgumentParser(description="Synthetic Text Image Generator")
    parser.add_argument("-lang", required=True, help="Path to dictionary .txt file")
    parser.add_argument("-w", type=int, default=3, help="Words per sample")
    parser.add_argument("-c", type=int, default=10, help="Number of samples")
    parser.add_argument("-bl", type=float, help="Specific blur amount")
    parser.add_argument("-rbl", action="store_true", help="Random blur")
    parser.add_argument("-b", type=str, choices=['0', '1', '2'], default='0')
    parser.add_argument("-rb", action="store_true", help="Random background")
    parser.add_argument("-k", type=float, help="Skew factor")
    parser.add_argument("-rk", action="store_true", help="Random skewing")
    parser.add_argument("-font", help="Specific font path")
    parser.add_argument("-font_dir", help="Directory of fonts")
    parser.add_argument("-color", default="#000000", help="Font color")
    parser.add_argument("-rcolor", action="store_true", help="Random font color")
    parser.add_argument("-out_dir", required=True, help="Output directory")
    args = parser.parse_args()

    # Prep folders
    img_dir = os.path.join(args.out_dir, "images_folder")
    os.makedirs(img_dir, exist_ok=True)
    words = load_dictionary(args.lang)

    with open(os.path.join(args.out_dir, "map.tsv"), 'w', encoding='utf-8') as tsv:
        for i in range(args.c):
            text = " ".join(random.sample(words, min(len(words), args.w)))
            font = get_font(args)
            
            # Measure text for canvas size
            temp_draw = ImageDraw.Draw(Image.new('RGB', (1,1)))
            bbox = temp_draw.textbbox((0, 0), text, font=font)
            size = (bbox[2] - bbox[0] + 40, bbox[3] - bbox[1] + 40)

            # Generate and Draw
            img = generate_background(args.b, args.rb, size)
            draw = ImageDraw.Draw(img)
            draw.text((20, 20), text, font=font, fill=get_font_color(args))
            
            # Post-processing
            img = apply_effects(img, args)

            # Save
            fname = f"sample_{i}.png"
            img.save(os.path.join(img_dir, fname))
            tsv.write(f"{fname}\t{text}\n")

    print(f"Successfully generated {args.c} images in {args.out_dir}")