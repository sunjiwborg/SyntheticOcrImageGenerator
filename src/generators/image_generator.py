from PIL import Image, ImageDraw

def get_image(text_layer, args):
    lw, lh = text_layer.size
    canvas_size = (lw + (args.m * 2), lh + (args.m * 2))

    bg_img = get_background_image(canvas_size)
    bg_img.paste(text_layer, (args.m, args.m), text_layer)
    final_img = bg_img

    return final_img

def get_background_image(canvas_size):
    return Image.new("RGB", canvas_size, (225, 225, 255))

