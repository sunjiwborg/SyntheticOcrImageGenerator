import os
import glob
import random
import numpy as np
from PIL import Image

def generate_background(bg_type_arg, is_random, size, bg_folder="project/background"):
    bg_type = bg_type_arg
    if is_random:
        bg_type = random.choice(['0', '1', '2'])

    if bg_type == '1': # Gaussian Noise
        array = np.full((size[1], size[0], 3), 255, dtype=np.uint8)
        noise = np.random.normal(0, 15, array.shape)
        noisy_array = np.clip(array + noise, 0, 255).astype(np.uint8)
        return Image.fromarray(noisy_array)
    
    elif bg_type == '2': # Image Background
        bg_files = glob.glob(os.path.join(bg_folder, "*.*"))
        if bg_files:
            with Image.open(random.choice(bg_files)) as img:
                return img.convert("RGB").resize(size, Image.Resampling.LANCZOS)
    
    # Default: Plain White
    return Image.new('RGB', size, (255, 255, 255))