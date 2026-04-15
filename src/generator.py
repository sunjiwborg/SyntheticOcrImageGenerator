import os
import random
from utils.text_utils import reader, get_font
from tqdm import tqdm
from PIL import Image, ImageDraw

def generator(args):
    # Read file 
    lines = reader(args.i)
    print(lines)
    # Setup output
    img_dir = os.path.join(args.o, "images")
    os.makedirs(img_dir, exist_ok=True)
    label_path = os.path.join(args.o, "labels.tsv")
    with open(label_path, 'w', encoding='utf-8') as tsv:
        for i in tqdm(range(len(lines)), desc="Generating Images", ascii=True, unit="img"):
            text = (lines[i])
            font = get_font(args)

            # Measure Text
            temp_draw = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
            bbox = temp_draw.textbbox((0,0), text, font=font)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

            # Render Text Layer
            text_layer = Image.new('RGBA', (tw + 10, th + 10), (0, 0, 0, 0))
            tdraw = ImageDraw.Draw(text_layer)
            tdraw.text((-bbox[0] + 5, -bbox[1] + 5), text, font=font, fill="black")

            # Canvas
            lw, lh = text_layer.size
            canvas_size = (lw +(args.margin * 2), lh +(args.margin * 2))
            
            bg_img = Image.new('RGB', canvas_size, (225, 225, 225))

            bg_img.paste(text_layer, (args.margin, args.margin), text_layer)

            final_img = bg_img
            # Save
            fname = f"sample_{i}.png"
            final_img.save(os.path.join(img_dir, fname))
            tsv.write(f"{fname}\t{text}\n")
        
    print(f"\nDone! Dataset saved to: {args.o}")
    