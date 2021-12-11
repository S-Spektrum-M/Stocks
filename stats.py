"""
Statistical Calculations for stock predictions
methods:
update_db
update_db_bad_id
calc_short
calc_long
short
long
curr
"""
import numpy as np
from robin_stocks import robinhood as rh
import auth
import redis
from datetime import datetime
from sklearn.linear_model import LinearRegression as lr

rh.authentication.login(auth.USERNAME, auth.PASSWORD)
CLIENT = redis.Redis(host='localhost', port=6379, db=0)


def update_db(query, vals):
    """
    Update the redis database with the latest predictions
    """
    CLIENT.set(query, "true")
    CLIENT.set(f'{query}.upper', vals[0])
    CLIENT.set(f'{query}.lower', vals[1])


def update_db_bad_id(ticker):
    """
    Update the redis database with the error
    """
    CLIENT.set(ticker, "bad_id")


def calc_short(y, i):
    """
    Use linear regression to calculate the upper and lower bounds
    """
    # calc LinearRegression of y
    x = np.arange(i)
    x = x.reshape(-1, 1)
    reg = lr().fit(x, y)
    # calculate upper and lower bounds
    pred = reg.predict(x)[0]
    return [round(pred * 1.05, 2), round(pred * 0.95, 2)]


def calc_long(y, i):
    """
    Use exponential curve fitting to calculate the upper and lower bounds
    """
    if y[0] != 0:
        rate_of_change = (y[i] / y[0])**(1 / float(i))
        return [
            round(y[i] * rate_of_change * 1.05, 2),
            round(y[i] * rate_of_change * 0.95, 2)
        ]
    return None


def short(ticker):
    """
    Return the short term upper and lower bounds for a stock
    """
    if CLIENT.get(ticker) != 'bad_id':
        query = (f'short-{ticker}-{datetime.now().strftime("%d/%m/%Y:%H")}')
        if CLIENT.get(query) != None:
            print(query)
            return [
                float(CLIENT.get(f'{query}.upper').decode('utf-8')),
                float(CLIENT.get(f'{query}.lower').decode('utf-8'))
            ]
        else:
            prices = rh.stocks.get_stock_historicals(ticker, 'hour', 'month')
            if prices[0] == None:
                update_db_bad_id(ticker)
                return None
            else:
                y_tmp = list()
                i = 0
                for price in prices:
                    y_tmp.append(float(price["open_price"]))
                    y_tmp.append(float(price["close_price"]))
                    i = i + 2

                b = calc_short(np.asarray(y_tmp), i)
                update_db(query, b)
                return b
    else:
        return None


def long(ticker):
    """
    Return the long term upper and lower bounds for a stock
    """
    if CLIENT.get(ticker) != 'bad_id':
        query = (f'long-{ticker}-{datetime.now().strftime("%d/%m/%Y")}')
        if CLIENT.get(query) != None:
            print(query)
            return [
                float(CLIENT.get(f'{query}.upper').decode('utf-8')),
                float(CLIENT.get(f'{query}.lower').decode('utf-8'))
            ]
        else:
            prices = rh.stocks.get_stock_historicals(ticker, 'day', '5year')
            if prices[0] == None:
                update_db_bad_id(ticker)
                return None
            else:
                y_tmp = list()
                i = -1
                for price in prices:
                    y_tmp.append(float(price["open_price"]))
                    y_tmp.append(float(price["close_price"]))
                    i = i + 2
                b = calc_long(np.asarray(y_tmp), i)
                if b != None:
                    update_db(query, b)
                return b
    else:
        return None


def current(ticker):
    """
    Return the current price for a stock
    """
    return rh.get_latest_price(ticker)[0]
