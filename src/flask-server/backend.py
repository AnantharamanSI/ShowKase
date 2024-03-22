import model
import preprocessor
import calcfunctions
import numpy as np
import json
from results import graph

def analyze_property(user_input):
    # Data should look like:
    # data = {"bed":1, "bath":1, "city":"Bronx", "state":"New York",
    #         "acre_lot":.11, "house_size":756, "date": 2007, "price":160000}
    data = json.loads(user_input)
    print("DATA LOGGED:", data, type(data))

    model.create()
    data["date"] = 2007
    price = data["price"]
    zest = price * 0.008
    appreciation_curr = calc_appreciation(data, price)
    appreciation_infl = np.array([calcfunctions.calc_inflation_adj(appreciation_curr[i], i) for i in range(11)]).astype(np.int64)
    depreciation = [calcfunctions.calc_depreciation(price, i) for i in range(11)]
    property_taxes = [calcfunctions.get_tax_amount(price, data["state"], i) for i in range(11)]
    mortgage = [calcfunctions.calc_mortage(price) * 12 * i for i in range(11)]

    total = np.array(appreciation_infl) + np.array(depreciation) - np.array(property_taxes) - np.array(mortgage)
    
    result = {
        "appreciation_curr": appreciation_curr,
        "appreciation_infl": appreciation_infl,
        "depreciation": depreciation,
        "property_taxes": property_taxes,
        "mortgage": mortgage,
        "total": total
    }  

    graph(result)

    result = {
        "appreciation_curr": appreciation_curr.astype(int).tolist(),
        "appreciation_infl": appreciation_infl.astype(int).tolist(),
        "depreciation": [int(i) for i in depreciation],
        "property_taxes": [int(i) for i in property_taxes],
        "mortgage": [int(i) for i in mortgage],
        "total": total.astype(int).tolist()
    }
    return result


def calc_appreciation(input_wide, price):

    input = preprocessor.transform(input_wide)
    prediction = model.predict(input)[0]
    price_predicted = preprocessor.transform_price(prediction)

    mult = price/price_predicted

    ret = np.zeros(11)
    for i in range(11):
        ret[i] = round(price_predicted * mult)
        input_wide["date"] += 1
        input = preprocessor.transform(input_wide)
        prediction = model.predict(input)[0]
        price_predicted = preprocessor.transform_price(prediction)
    
    return ret