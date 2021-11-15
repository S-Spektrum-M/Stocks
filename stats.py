import numpy as np
import statistics as stat
from robin_stocks import robinhood as rh
import auth

rh.authentication.login(auth.USERNAME, auth.PASSWORD)

def short_linear_reg(ticker):
    """
    param: ticker: string that represents ticker to query
    return: short term linear regression prediction
    """
    prices = rh.stocks.get_stock_historicals(ticker, 'hour', 'month')

    y_tmp = list()
    i = 0
    for price in prices:
        y_tmp.append(float(price["open_price"]))
        y_tmp.append(float(price["close_price"]))
        i = i + 2

    x = np.arange(0, i)
    y = np.asarray(y_tmp)

    r = np.corrcoef(x, y)[0][1]
    s_x = np.std(x)
    s_y = np.std(y)
    slope = r * s_y / s_x
    return [slope * (i+1 - np.mean(x)) + np.mean(y) + (s_y), slope * (i+1 - np.mean(x)) + np.mean(y) - (s_y)]

def long_linear_reg(ticker):
    """
    param: ticker: string that represents ticker to query
    return: long term linear regression prediction
    """
    prices = rh.stocks.get_stock_historicals(ticker, 'day', '5year')

    y_tmp = list()
    i = 0
    for price in prices:
        y_tmp.append(float(price["open_price"]))
        y_tmp.append(float(price["close_price"]))
        i = i + 2

    x = np.arange(0, i)
    y = np.asarray(y_tmp)

    r = np.corrcoef(x, y)[0][1]
    s_x = np.std(x)
    s_y = np.std(y)
    slope = r * s_y / s_x
    return [slope * (i+1 - np.mean(x)) + np.mean(y) + (s_y), slope * (i+1 - np.mean(x)) + np.mean(y) - (s_y)]
