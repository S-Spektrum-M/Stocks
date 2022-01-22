"""
Statistical Calculations for stock predictions
methods:
_update_db
_update_db_bad_id
calc_short
calc_long
short
long
curr
"""

from datetime import datetime
import numpy as np
from robin_stocks import robinhood as rh
from sklearn.linear_model import LinearRegression as lr
import redis
import auth

rh.authentication.login(auth.get_username(), auth.get_password())
CLIENT = redis.Redis(host='localhost', port=6379, db=0)


def _update_db(query, vals):
    """
    Update the redis database with the latest predictions
    """
    CLIENT.set(query, "true")
    CLIENT.set(f'{query}.upper', vals[0])
    CLIENT.set(f'{query}.lower', vals[1])


def _update_db_bad_id(ticker):
    """
    Update the redis database with the error
    """
    CLIENT.set(ticker, "bad_id")


def calc_short(historicals, i):
    """
    Use linear regression to calculate the upper and lower bounds
    """
    # calc LinearRegression of historicals
    features = np.arange(i)
    features = features.reshape(-1, 1)
    reg = lr().fit(features, historicals)
    # calculate upper and lower bounds
    pred = reg.predict(features)[0]
    return [round(pred * 1.05, 2), round(pred * 0.95, 2)]


def calc_long(historicals, i):
    """
    Use exponential curve fitting to calculate the upper and lower bounds
    """
    if historicals[0] != 0:
        rate_of_change = (historicals[i] / historicals[0])**(1 / float(i))
        return [
            round(historicals[i] * rate_of_change * 1.05, 2),
            round(historicals[i] * rate_of_change * 0.95, 2)
        ]
    return None


def short(ticker):
    """
    Return the short term upper and lower bounds for a stock
    """
    if CLIENT.get(ticker) != 'bad_id':
        query = (f'short-{ticker}-{datetime.now().strftime("%d/%m/%Y:%H")}')
        if CLIENT.get(query) is not None:
            print(query)
            return [
                float(CLIENT.get(f'{query}.upper').decode('utf-8')),
                float(CLIENT.get(f'{query}.lower').decode('utf-8'))
            ]
        prices = rh.stocks.get_stock_historicals(ticker, 'hour', 'month')
        if prices[0] is None:
            _update_db_bad_id(ticker)
            return None
        y_tmp = list()
        i = 0
        for price in prices:
            y_tmp.append(float(price["open_price"]))
            y_tmp.append(float(price["close_price"]))
            i = i + 2

        ret_arr = calc_short(np.asarray(y_tmp), i)
        _update_db(query, ret_arr)
        return ret_arr
    return None


def long(ticker):
    """
    Return the long term upper and lower bounds for a stock
    """
    if CLIENT.get(ticker) != 'bad_id':
        query = (f'long-{ticker}-{datetime.now().strftime("%d/%m/%Y")}')
        if CLIENT.get(query) is not None:
            print(query)
            return [
                float(CLIENT.get(f'{query}.upper').decode('utf-8')),
                float(CLIENT.get(f'{query}.lower').decode('utf-8'))
            ]
        prices = rh.stocks.get_stock_historicals(ticker, 'day', '5year')
        if prices[0] is None:
            _update_db_bad_id(ticker)
            return None
        y_tmp = list()
        i = -1
        for price in prices:
            y_tmp.append(float(price["open_price"]))
            y_tmp.append(float(price["close_price"]))
            i = i + 2
        ret_arr = calc_long(np.asarray(y_tmp), i)
        if ret_arr is not None:
            _update_db(query, ret_arr)
        return ret_arr
    return None


def current(ticker):
    """
    Return the current price for a stock
    """
    return rh.get_latest_price(ticker)[0]
