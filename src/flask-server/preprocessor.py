import pandas as pd
import numpy as np
import pickle
import os

dir_path = os.path.dirname(os.path.abspath(__file__))

def load_data(fp):
    df = pd.read_csv(fp, index_col=None, na_values=['NA'],header=None,low_memory=False)
    df = df.dropna()
    df = df[1:].to_numpy()
    df = df.T
    df[8] = [string[:4] for string in df[8]]
    return df

def normalize(data, norm_data, label): 
    data = data.astype(np.float64).astype(np.int64)
    med = np.median(data)
    std = np.std(data)
    data = (data - med)/std
    norm_data[label] = (med, std)
    return data

def one_hot(arr):
    unique, inverse = np.unique(arr, return_inverse=True)
    onehot = np.eye(unique.shape[0])[inverse]
    encoding = {}
    for i in range(len(unique)):
        encoding[unique[i]] = i
    with open(os.path.join(dir_path,"../../model/model.dat"), "wb") as f:
        pickle.dump(encoding, f)
    return onehot

def numericize(arr):
    encoding = {}
    retval = np.zeros(len(arr))
    num = 0
    for i in range(len(arr)):
        if arr[i] not in encoding:
            encoding[arr[i]] = num
            num += 1
        retval[i] = encoding[arr[i]]
    with open(os.path.join(dir_path,"../../model/city_encoding.dat"), "wb") as f:
        pickle.dump(encoding, f)
    return retval

def preprocess(fp):
    norm_data = {}
    df = load_data(fp)
    price = normalize(df[9], norm_data, "price")
    bed= normalize(df[1], norm_data, "bed")
    bath = normalize(df[2], norm_data, "bath")
    acre_lot = normalize(df[3], norm_data, "acre_lot")
    house_size = normalize(df[7], norm_data, "house_size")
    city = normalize(numericize(df[4]), norm_data, "city")
    state = one_hot(df[5])
    date = normalize(df[8], norm_data, "date")
    data = [bed, bath, acre_lot, city, house_size, date]
    data.extend(state.T)
    data = np.array(data).T
    with open(os.path.join(dir_path,"../../model/model.dat"), "wb") as f:
        pickle.dump(norm_data, f)
    return data, price

def transform(data):
    with open(os.path.join(dir_path,"../../model/norms.dat"), "rb") as f:
        norm_data = pickle.load(f)
    with open(os.path.join(dir_path ,"../../model/city_encoding.dat"), "rb") as f:
        city_encoding = pickle.load(f)
    with open(os.path.join(dir_path,"../../model/state_encoding.dat"), "rb") as f:
        state_encoding = pickle.load(f)

    bed = (data["bed"] - norm_data["bed"][0])/norm_data["bed"][1]
    bath = (data["bath"] - norm_data["bath"][0])/norm_data["bath"][1]
    acre_lot = (data["acre_lot"] - norm_data["acre_lot"][0])/norm_data["acre_lot"][1]
    house_size = (data["house_size"] - norm_data["house_size"][0])/norm_data["house_size"][1]
    if data["city"] in city_encoding:
        city = city_encoding[data["city"]]
    else:
        city = norm_data["city"][0]
    city = (city - norm_data["city"][0])/norm_data["city"][1]
    state_arr = np.zeros(len(state_encoding))
    if data["state"] in state_encoding:
        state_arr[state_encoding[data["state"]]] = 1
    date = (data["date"] - norm_data["date"][0])/norm_data["date"][1]
    ret = [bed, bath, acre_lot, city, house_size, date]
    ret.extend(state_arr)
    return ret

def transform_price(prediction):
    with open(os.path.join(dir_path, "../../model/norms.dat"), "rb") as f:
        norm_data = pickle.load(f)
    price = prediction * norm_data["price"][1] + norm_data["price"][0]
    return price
