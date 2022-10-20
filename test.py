import matplotlib.pyplot as plt
from pbn.paint_by_numbers import PaintByNumbers


IMAGE_PATHS = ["still_life", "cobra", "parrots", "beach_landscape", "madiba"]

for image in IMAGE_PATHS:
    still_life_obj = PaintByNumbers(img_path=f"./images/{image}.jpg", num_of_colors=12)
    proc_img = still_life_obj.image_preprocessing()
    quant_img = still_life_obj.quantise_image(img_array=proc_img)
    out_img = still_life_obj.outline_and_label_image()