from damage_detection.subroutines.HDF5 import HDF5DatasetGeneratorMask
from damage_detection.config_class import Config

import sys
import os


def predict(model):
    folder = {}
    # Use this to easily run the code in different directories/devices
    folder['initial'] = ''
    # The path where the repository is stored
    # folder['main'] = folder['initial'] + './'
    folder['main'] = './damage_detection/'

    # if folder['main'] == '', then the current working directory will be used
    if folder['main'] == '':
        folder['main'] = os.getcwd()

    sys.path.append(folder['main'])

    cnf = Config(folder['main'])
    args = cnf.set_repository()

    # Set some parameters
    IMAGE_DIMS = cnf.IMAGE_DIMS
    BS = cnf.BS

    # Do not use data augmentation when evaluating model: aug=None
    evalGen = HDF5DatasetGeneratorMask(args['EVAL_HDF5'], BS, aug=None, shuffle=False, binarize=args['binarize'])

    # Use the pretrained model to fenerate predictions for the input samples from a data generator
    predictions = model.predict_generator(evalGen.generator(),
                                            steps=evalGen.numImages // BS+1, max_queue_size=BS * 2, verbose=1)
    evalGen.close()
    # Define folder where predictions will be stored
    predictions_folder = '{}{}/'.format(args['predictions'], args['pretrained_filename'])
    # Create folder where predictions will be stored
    cnf.check_folder_exists(predictions_folder)

    # Show the metrics for the prediction
    from subroutines.visualize_predictions import Visualize_Predictions
    return Visualize_Predictions(args, predictions)
