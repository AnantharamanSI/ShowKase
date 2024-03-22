from sklearn.neural_network import MLPRegressor as regressor
import preprocessor
import model
import pickle
import os

dir_path = os.path.dirname(os.path.abspath(__file__))

def train(X, y):
   
    regr = regressor(hidden_layer_sizes = (50, 30, 10),
                      max_iter = 500,
                      verbose = False,
                      activation = "relu",
                      warm_start = True,
                      n_iter_no_change = 20)
    regr.fit(X, y)
    return regr

def create():
    if os.path.exists(os.path.join(dir_path,"../../model/model.dat")):
        return
    
    attributes, targets = preprocessor.preprocess(os.path.join(dir_path, "../../data/realtor-data.csv"))
    trained_model = model.train(attributes, targets)

    with open(os.path.join(dir_path,"../../model/model.dat"), "wb") as f:
        pickle.dump(trained_model, f)

def predict(property_params):
    if not os.path.exists(os.path.join(dir_path,"../../model/model.dat")):
        return None
    
    with open(os.path.join(dir_path,"../../model/model.dat"), "rb") as f:
        regr = pickle.load(f)
    
    if regr:
        return regr.predict([property_params])
    else:
        return None
