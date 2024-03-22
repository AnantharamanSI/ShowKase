import sys
import numpy as np
import h5py
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable 

def Visualize_Predictions(args, predictions, threshold=0.5):
    """
    threshold: use this value to binarize the ground trough mask
    """
    
    sys.path.append(args["main"])
     
    # Load database with images and masks
    db = h5py.File(args['EVAL_HDF5'], 'r+')
    numImages = db["images"].shape[0]    

    # Show the crack as grey    
    color = 0.5 # 0.5:grey, 1: white
     
    # Size of plot
    plt_size = [3, 3]
    
    mask_tiles = []
    damage_counts = []
    # Loop over the images and produce a plot with original image, ground truth and prediction
    for ii in range (0, numImages):
        
        # Filename to store plot for each image
        plt_file = '{}{}.png'.format(args['predictions_subfolder'], ii)

        # Ground truth
        # gt = (db["labels"][ii].squeeze())*color
        
        # Define im array
        im = (np.zeros(db["images"][ii].shape)).astype('uint8') 
        im[:,:,0] = (db["images"][ii][:,:,2] * 255) .astype('uint8') 
        im[:,:,1] = (db["images"][ii][:,:,1] * 255) .astype('uint8') 
        im[:,:,2] = (db["images"][ii][:,:,0] * 255) .astype('uint8') 
    
        plt_subtitle = ''
    
        # Create figure with 3 subplots
        # fig = plt.figure()
        # fig.set_size_inches(plt_size)
        # ax1 = plt.subplot2grid((1,1), (0,0))
        # divider = make_axes_locatable(ax1) 
        # ax3 = divider.append_axes("bottom", size="100%", pad=0.4)
        
        # Original image
        # ax1.imshow(im)

        # Prediction     
        prediction = ((predictions[ii].squeeze()>threshold)*1)*color 
        damage_count = np.sum(np.array(prediction) >= 0.5)
    
        mask_tiles.append(prediction)
        damage_counts.append(damage_count)

        # ax3.imshow(prediction, vmin=0, vmax=1, cmap='gray')
        
        # # Set title for prediction
        # ax3.set_title(plt_subtitle, fontsize=7)  
        
        # # Remove axes
        # ax1.axis('off')  
        # ax3.axis('off') 
    
        # plt.tight_layout()
        # plt.savefig(plt_file, bbox_inches = "tight", dpi=100, pad_inches=0.05) 
        # plt.close()

    return mask_tiles, damage_counts
        