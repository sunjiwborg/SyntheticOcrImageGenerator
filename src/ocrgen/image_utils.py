import random
from PIL import Image, ImageFilter

def apply_rotation_to_layer(text_layer, angle):
    """Rotates the text layer (tilt) without cropping."""
    return text_layer.rotate(angle, resample=Image.BICUBIC, expand=True)

def apply_blur_to_final(image, args):
    """Applies blur to the final composited image."""
    if args.rbl:
        return image.filter(ImageFilter.GaussianBlur(radius=random.choice([0, 1, 2])))
    elif args.bl is not None:
        return image.filter(ImageFilter.GaussianBlur(radius=args.bl))
    return image

def get_font_color(args):
    if args.rcolor:
        return (random.randint(0, 150), random.randint(0, 150), random.randint(0, 150))
    return args.color