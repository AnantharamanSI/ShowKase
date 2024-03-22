import os
  
class Config:
    def __init__(self, working_folder):
        # The path where the repository is stored
        self.working_folder = working_folder
        # Info that will be used as prefix of any output files
        self.info = 'crack_detection'
        # Dimensions of the images that will be fed to the network
        self.IMAGE_DIMS = (224 , 224 , 3)
        # Batch size
        self.BS = 4
        # The parameters of the configuration used will be stored in the dictionary args
        self.args = {}
        # Whether data generators will binarize masks 
        self.args['binarize'] = True # True or False
        
        
    def check_folder_exists(self, folder_path):
        """ 
        check if folder exists and if not create it
        """
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def set_repository(self):
        
        # Pass the path where the repository is stored to the args
        self.args['main'] = self.working_folder
        # Where the dataset is stored
        self.args['dataset'] = os.path.join(self.args['main'], 'dataset/')
        # A new folder will be created where any output will be stored in
        self.args['output'] = os.path.join(self.args['main'], 'output/')
        # The dataset will be stored in HDF5 format here
        self.args['hdf5'] = os.path.join(self.args['output'], 'hdf5/')
        # The saved model will be stored here
        self.args['checkpoints'] = os.path.join(self.args['output'], 'checkpoints/')
        # The saved weights will be stored here        
        self.args['weights'] = os.path.join(self.args['output'], 'weights/')
        # Theserialized model (JSON) will be stored here
        self.args['model_json_folder'] = os.path.join(self.args['output'], 'model_json/')
        # Predictions will be stored here
        self.args['predictions'] = os.path.join(self.args['output'], 'predictions/')
        
        # Create the folders
        folders = [self.args['hdf5'], self.args['checkpoints'], self.args['weights'], 
                   self.args['model_json_folder'], self.args['predictions']]
        for f in (folders):
            self.check_folder_exists(f)

        # Save the HDF5 file to different folder according to IMAGE_DIMS
        temp = '{}_{}_{}_{}/'.format(self.info, self.IMAGE_DIMS[0],self.IMAGE_DIMS[1],self.IMAGE_DIMS[2])
        self.check_folder_exists(self.args['hdf5'] + temp)
     
        # define the EVAL_HDF5 suitably
        self.args['EVAL_HDF5'] = self.args['hdf5'] + temp + 'val.hdf5'
            
        # Define the path that the patches of images and masks are stored
        self.args['raw_images'] = self.args['main'] + 'raw_images/'
        self.args['images'] = self.args['dataset'] + '{}_{}_images/'.format(self.info, self.IMAGE_DIMS[0])
    
        # Define the file with the pretrained weights or the model with weights that will be used to evaluate model
        # e.g. 'crack detection_1_epoch_7_F1_score_dil_0.762.h5'
        self.args['pretrained_filename'] = 'crack_detection_weights.h5'
        # Define the subfolder where predictions will be stored
        self.args['predictions_subfolder'] = '{}{}/'.format(self.args['predictions'], self.args['pretrained_filename'])
        # Define whether to dilate ground truth mask for the calculation of Precision metric
        # Background pixels predicted as cracks (FP) are considered as TP if they are a few 
        # pixels apart from the annotated cracks. Refer to the Journal paper for extra clarification                 
        self.args['predictions_dilate'] = True # True or False
        # The path for the serialized model to JSON
        self.args['model_json'] = self.args['model_json_folder'] + self.info + '.json' 
        
        return self.args