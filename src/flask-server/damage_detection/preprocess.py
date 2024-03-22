import os
import io

folder = {}
# Use this to easily run the code in different directories/devices
folder['initial'] = ''
# The path where the repository is stored
folder['main'] = folder['initial'] + './'

# if folder['main'] == '', then the current working directory will be used
if folder['main'] == '':
    folder['main'] = os.getcwd()
folder['main'] = './damage_detection/'


import sys
sys.path.append(folder["main"])

from damage_detection.config_class import Config

cnf = Config(folder["main"])
args = cnf.set_repository()

# Set some parameters
IMAGE_DIMS = cnf.IMAGE_DIMS

from skimage.transform import resize
from skimage import data
from imutils import paths
import numpy as np
import progressbar
import cv2
from PIL import Image
from damage_detection.subroutines.HDF5 import HDF5DatasetWriterMask


def segment_img(img_path):
    img_bytes = img_path.read()
    img = Image.open(io.BytesIO(img_bytes))
    img.thumbnail((600, 600)) # Resize image so that it's quick to process
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    M, N = 224, 224
    tiles = [img[x:x+M,y:y+N] for x in range(0,img.shape[0],M) for y in range(0,img.shape[1],N)]
    return tiles, img.shape


def store_img_hdf5(tiles):
 
    # construct a list pairing the evaluation image paths along 
    # with their corresponding labels and output HDF5 files
    datasets = [(tiles, args['EVAL_HDF5'])]


    # loop over the dataset tuples
    for (images, outputPath) in datasets:
        
        # create HDF5 writer
        print("[INFO] building {}...".format(outputPath))
        writer = HDF5DatasetWriterMask((len(images), IMAGE_DIMS[0], IMAGE_DIMS[1], IMAGE_DIMS[2]), outputPath)

        # initialize the progress bar
        widgets = ["Building Dataset: ", progressbar.Percentage(), " ",
                progressbar.Bar(), " ", progressbar.ETA()]
        pbar = progressbar.ProgressBar(maxval=len(images),
                                    widgets=widgets).start()
        
        # loop over the image paths
        for (ii, image) in enumerate(images):
                        
            # resize image if dimensions are different
            if IMAGE_DIMS != image.shape:
                image = resize(image, (IMAGE_DIMS), mode='constant', preserve_range=True)
            
            # normalize intensity values: [0,1]
            image = image / 255
            
            # add the image and label to the HDF5 dataset
            writer.add([image])
            
            # update progress bar
            pbar.update(ii)
        
        # close the progress bar and the HDF5 writer
        pbar.finish()   
        writer.close()


def process(img_path):
    tiles, shape = segment_img(img_path)
    store_img_hdf5(tiles)

    return shape