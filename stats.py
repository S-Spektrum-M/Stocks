import numpy as np
from robin_stocks import robinhood as rh
import auth
import redis
from datetime import datetime
from numba import njit

rh.authentication.login(auth.USERNAME, auth.PASSWORD)
client = redis.Redis(host='localhost', port=6379, db=0)
now = datetime.now()

@njit()
def calc_short(y, i):
    x = np.arange(0, i)
    r = np.corrcoef(x, y)[0][1]
    s_x = np.std(x)
    s_y = np.std(y)
    slope = r * s_y / s_x
    b = [
        round(slope * (i+1 - np.mean(x)) + np.mean(y) + (s_y), 2),
        round(slope * (i+1 - np.mean(x)) + np.mean(y) - (s_y), 2)
    ]
    return b

@njit()
def calc_long(y, i):
    if y[0] != 0:
        rate_of_change = (y[i]/y[0]) ** (1/float(i))
        b = [
            round(y[i] * rate_of_change + np.std(y),2),
            round(y[i] * rate_of_change - np.std(y),2),
        ]
        return b
    else:
        return None

def update_db(query, vals):
    client.set(query, "true")
    client.set(f'{query}.upper',vals[0])
    client.set(f'{query}.lower',vals[1])

def short(ticker):
    query = (f'short-{ticker}-{datetime.now().strftime("%d/%m/%Y:%H")}')
    if client.get(query) != None:
        print(query)
        return [
            float(client.get(f'{query}.upper').decode('utf-8')),
            float(client.get(f'{query}.lower').decode('utf-8'))
        ]
    else:
        prices = rh.stocks.get_stock_historicals(ticker, 'hour', 'month')
        if prices[0] == None:
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

def long(ticker):
    query = (f'long-{ticker}-{datetime.now().strftime("%d/%m/%Y")}')
    if client.get(query) != None:
        print(query)
        return [
            float(client.get(f'{query}.upper').decode('utf-8')),
            float(client.get(f'{query}.lower').decode('utf-8'))
        ]
    else:
        prices = rh.stocks.get_stock_historicals(ticker, 'day', '5year')
        if prices[0] == None:
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
