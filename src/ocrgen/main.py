import argparse
import os
import random
from PIL import Image, ImageDraw
from .text_utils import load_dictionary, get_font
from .image_utils import apply_rotation_to_layer, apply_blur_to_final, get_font_color
from .bg_utils import generate_background

def main():
    parser = argparse.ArgumentParser(description="OCR-Gen: Synthetic Text Image Generator")
    parser.add_argument("-lang", required=True)
    parser.add_argument("-w", type=int, default=3)
    parser.add_argument("-c", type=int, default=10)
    
    # Text Appearance
    parser.add_argument("-pt", type=int, default=32)
    parser.add_argument("-rpt", type=int, nargs=2, metavar=('MIN', 'MAX'))
    parser.add_argument("-color", default="#000000")
    parser.add_argument("-rcolor", action="store_true")
    parser.add_argument("-margin", type=int, default=10)
    
    # Backgrounds
    parser.add_argument("-b", type=str, choices=['0', '1', '2'], default='0')
    parser.add_argument("-rb", action="store_true")
    parser.add_argument("-bg_dir", default="backgrounds")
    
    # Effects (Skew removed, Tilt remains)
    parser.add_argument("-t", type=float, help="Specific tilt/rotation angle")
    parser.add_argument("-rt", action="store_true", help="Random tilt (-10 to 10 degrees)")
    parser.add_argument("-bl", type=float)
    parser.add_argument("-rbl", action="store_true")
    
    # Fonts & Output
    parser.add_argument("-font", help="Path to specific font")
    parser.add_argument("-font_dir", help="Directory for random font selection")
    parser.add_argument("-out_dir", required=True)
    
    args = parser.parse_args()

    img_dir = os.path.join(args.out_dir, "images_folder")
    os.makedirs(img_dir, exist_ok=True)
    words = load_dictionary(args.lang)

    with open(os.path.join(args.out_dir, "map.tsv"), 'w', encoding='utf-8') as tsv:
        for i in range(args.c):
            text = " ".join(random.sample(words, min(len(words), args.w)))
            font = get_font(args)
            
            # 1. Measure text for the initial layer
            temp_draw = ImageDraw.Draw(Image.new('RGBA', (1,1)))
            bbox = temp_draw.textbbox((0, 0), text, font=font)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

            # 2. Create Transparent Text Layer
            # Buffer added to prevent clipping during rotation
            text_layer = Image.new('RGBA', (tw + 10, th + 10), (0, 0, 0, 0))
            tdraw = ImageDraw.Draw(text_layer)
            tdraw.text((-bbox[0] + 5, -bbox[1] + 5), text, font=font, fill=get_font_color(args))

            # 3. Apply Tilt/Rotation only
            if args.rt or args.t is not None:
                angle = args.t if not args.rt else random.uniform(-10, 10)
                text_layer = apply_rotation_to_layer(text_layer, angle)

            # 4. Final Canvas Calculation
            lw, lh = text_layer.size
            canvas_size = (lw + (args.margin * 2), lh + (args.margin * 2))

            # 5. Composite Text onto Background
            bg_img = generate_background(args.b, args.rb, canvas_size, args.bg_dir)
            bg_img.paste(text_layer, (args.margin, args.margin), text_layer)

            # 6. Final Blur and Save
            final_img = apply_blur_to_final(bg_img, args)
            fname = f"sample_{i}.png"
            final_img.save(os.path.join(img_dir, fname))
            tsv.write(f"{fname}\t{text}\n")

    print(f"Successfully generated {args.c} images in {args.out_dir}")

if __name__ == "__main__":
    main()