import os
from tqdm import tqdm
from cli import cli
from generators.text_generator import get_text_layer
from generators.image_generator import get_image
def main():
    args = cli()
    
    # Read lines of text
    with open(args.i, "r", encoding="utf-8") as f:
        total_lines = sum(1 for _ in f)
    with open(args.i, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in tqdm(f, total=total_lines, desc="Reading lines of text...", ascii=True, unit="line") if line.strip()]
    
    # Setup output
    img_dir = os.path.join(args.o, "images")
    os.makedirs(img_dir, exist_ok=True)
    label_path = os.path.join(args.o, "labels.tsv")
    
    # Main loop
    with open(label_path, "w", encoding="utf-8") as tsv:
        for i in tqdm(range(len(lines)), desc="Generating Images", ascii=True, unit="img"):
            text = lines[i]
            text_layer = get_text_layer(text, args)
            final_img = get_image(text_layer, args)

            # Save
            img_filename = f"{i}.png"
            img_path = os.path.join(img_dir, img_filename)
            final_img.save(img_path)
            tsv.write(f"{img_filename}\t{text}\n")

if __name__ == "__main__" :
    main()