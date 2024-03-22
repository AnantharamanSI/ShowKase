from keras.models import model_from_json

class LoadModel:
    def __init__(self, args, IMAGE_DIMS, BS):
        self.args = args
        self.IMAGE_DIMS = IMAGE_DIMS
        self.BS = BS

    def load_pretrained_model(self):
        """
        Load a pretrained model
        """

        # load json and create model
        json_file = open(self.args['model_json'], 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        try:
            model = model_from_json(loaded_model_json)
        except Exception as e:
            print("ERROR: ", e)
    
        # load weights into new model
        model.load_weights(self.args['weights'] + self.args['pretrained_filename'])
    
        return model