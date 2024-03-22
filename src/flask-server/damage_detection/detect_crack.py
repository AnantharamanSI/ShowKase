import os
import sys
import numpy as np
import cv2

from damage_detection import preprocess, model_inference
from damage_detection.config_class import Config
from damage_detection.evaluate_class import LoadModel

from math import ceil
import io
from PIL import Image
import base64

from os.path import dirname, abspath
d = dirname(dirname(abspath(__file__)))
sys.path.append(d)

folder = {}

folder['main'] = dirname(abspath(__file__))

import sys
sys.path.append(folder["main"])

from damage_detection.config_class import Config

cnf = Config(folder["main"])
args = cnf.set_repository()

# Set some parameters
IMAGE_DIMS = cnf.IMAGE_DIMS
BS = cnf.BS

def reconstruct_img(mask_tiles, shape):
    # Calculate the dimensions of the original image
    img_height = IMAGE_DIMS[0] * ceil(shape[0]/IMAGE_DIMS[0])
    img_width = IMAGE_DIMS[1] * ceil(shape[1]/IMAGE_DIMS[1])


    # Initialize an empty array to store the reconstructed image
    reconstructed_img = np.zeros((img_height, img_width), dtype=mask_tiles[0].dtype)

    row_idx = 0
    col_idx = 0
    # Iterate through each tile and place it in the reconstructed image
    for i, tile in enumerate(mask_tiles):
        
        # Calculate the row and column indices to place the tile
        reconstructed_img[row_idx:row_idx+IMAGE_DIMS[0], col_idx:col_idx+IMAGE_DIMS[1]] = tile
        col_idx += IMAGE_DIMS[1]
        if col_idx >= img_width:
            col_idx = 0
            row_idx += IMAGE_DIMS[0]        
        
    return reconstructed_img

def get_damage(damages):
    total = 0
    for i in damages:
        total += i/ (224*224)
    return total

def detect_damage(images):
    model = LoadModel(args, IMAGE_DIMS, BS).load_pretrained_model()

    # imgPaths = list(paths.list_images(args['raw_images']))
    damages = []
    masks = []
    image_outs = []
    for i, img_path in enumerate(images):
        if img_path:
        # Segment images into tile
        # Store image in HDF5 database
            shape = preprocess.process(img_path)
            mask_tiles, damage_counts = model_inference.predict(model)
            recon_img = reconstruct_img(mask_tiles, shape)

            pred_mask_path = os.path.join(folder['main'], 'pred_masks')
            if not os.path.exists(pred_mask_path):
                os.makedirs(pred_mask_path)

            img = 255*recon_img
            masks.append(img)
            damages.append(get_damage(damage_counts))

            if not cv2.imwrite(os.path.join(pred_mask_path, str(i)+'_mask.png'), 255*img):
                raise Exception("Could not write image")
            print('damage for', i, get_damage(damage_counts))

            rawBytes = io.BytesIO()
            im = Image.fromarray(img.astype("uint8"))
            im.save(rawBytes, "JPEG")
            image_outs.append(base64.b64encode(rawBytes.getvalue()).decode('utf-8').replace('+', '$'))
    

    return image_outs, damages