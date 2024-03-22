import pickle
import os

dir_path = os.path.dirname(os.path.abspath(__file__))

def calc_depreciation(price, time):
    if time < 27.5:
        return time*.03636 * price
    return price

def calc_mortage(price):
     time = 10
     monthly_payment = price * (.0544/12 * (1 + .0544/12) ** 12*time)/((1 + .0544/12) ** 12*time - 1)
     return monthly_payment
    

def calc_inflation_adj(price, year):
    return price*(1+.034)**year

def calc_rental_income(price, zestimate, time):
    rent = 0
    for i in range(time):
        rent = rent + (calc_inflation_adj(price, time))*(zestimate/price)
    return rent

def get_tax_amount(price, state, time):
    f = open(os.path.join(dir_path, "../../data/tax_rates.dat"), "rb")
    rates = pickle.load(f)
    f.close()
    tax = 0
    for i in range(time):
        tax = tax + (calc_inflation_adj(price, i)) * rates[state]
    return tax
