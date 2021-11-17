import numpy as np
import statistics as stat
from robin_stocks import robinhood as rh
import auth
import redis
from datetime import datetime

rh.authentication.login(auth.USERNAME, auth.PASSWORD)
client = redis.Redis(host='localhost', port=6379, db=0)
now = datetime.now()


def short_linear_reg(ticker):
    """
    param: ticker: string that represents ticker to query
    return: short term linear regression prediction
    """
    try:
        prices = rh.stocks.get_stock_historicals(ticker, 'hour', 'month')
    except TypeError:
        return [0,0].append("bad_request")

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

    query = (f'short-{ticker}-{datetime.now().strftime("%H:%M")}')
    if (client.get(query)) == None:
        b = [slope * (i+1 - np.mean(x)) + np.mean(y) + (s_y), slope * (i+1 - np.mean(x)) + np.mean(y) - (s_y)]
        client.set(query,str(b))
        print(f'Added {ticker} to db')
        return b
    else:
        print(f'loaded {ticker} from db')
        print(query)
        return client.get(query)

def long_linear_reg(ticker):
    """
    param: ticker: string that represents ticker to query
    return: long term linear regression prediction
    """
    try:
        prices = rh.stocks.get_stock_historicals(ticker, 'day', '5year')
    except TypeError:
        return [0,0].append("bad_request")

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

    query = (f'long-{ticker}-{datetime.now().strftime("%H:%M")}')
    if (client.get(query)) == None:
        b = [slope * (i+1 - np.mean(x)) + np.mean(y) + (s_y), slope * (i+1 - np.mean(x)) + np.mean(y) - (s_y)]
        client.set(query,str(b))
        print(f'Added {ticker} to db')
        return b
    else:
        print(f'loaded {ticker} from db')
        print(query)
        return client.get(query)
