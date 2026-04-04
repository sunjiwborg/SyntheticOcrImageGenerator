import random
import numpy as np
from PIL import Image, ImageFilter

def apply_effects(image, args):
    # Gaussian Blur
    if args.rbl:
        image = image.filter(ImageFilter.GaussianBlur(radius=random.choice([0, 1, 2])))
    elif args.bl is not None:
        image = image.filter(ImageFilter.GaussianBlur(radius=args.bl))
    
    # Skewing (Affine Transform)
    if args.rk or args.k is not None:
        k_val = args.k if not args.rk else random.uniform(-0.5, 0.5)
        width, height = image.size
        affine_matrix = (1, k_val, 0, 0, 1, 0)
        image = image.transform(
            (int(width + abs(k_val * height)), height), 
            Image.AFFINE, affine_matrix, Image.BICUBIC, fillcolor=(255, 255, 255)
        )
    return image

def get_font_color(args):
    if args.rcolor:
        return (random.randint(0, 150), random.randint(0, 150), random.randint(0, 150))
    return args.color