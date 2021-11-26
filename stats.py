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
    query = (f'short-{ticker}-{datetime.now().strftime("%H:%M")}')
    if client.get(query) != None:
        print(f'loaded {ticker} from db')
        print(query)
        return [
            float(client.get(f'{query}.upper').decode('utf-8')),
            float(client.get(f'{query}.lower').decode('utf-8'))
        ]
    else:
        try:
            prices = rh.stocks.get_stock_historicals(ticker, 'hour', 'month')
        except TypeError:
            return None

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
        b = [
            round(slope * (i+1 - np.mean(x)) + np.mean(y) + (s_y), 2),
            round(slope * (i+1 - np.mean(x)) + np.mean(y) - (s_y), 2)
        ]

        client.set(query, "true")
        client.set(f'{query}.upper',b[0])
        client.set(f'{query}.lower',b[1])
        print(f'Added {ticker} to db')
        return b

def long_linear_reg(ticker):
    query = (f'long-{ticker}-{datetime.now().strftime("%H:%M")}')
    if client.get(query) != None:
        print(f'loaded {ticker} from db')
        print(query)
        return [
            float(client.get(f'{query}.upper').decode('utf-8')),
            float(client.get(f'{query}.lower').decode('utf-8'))
        ]
    else:
        try:
            prices = rh.stocks.get_stock_historicals(ticker, 'day', '5year')
        except TypeError:
            return None

        y_tmp = list()
        i = -1
        for price in prices:
            y_tmp.append(float(price["open_price"]))
            y_tmp.append(float(price["close_price"]))
            i = i + 2

        rate_of_change = y_tmp[i] ** (1/float(i))
        b = [
            round(y_tmp[i] * rate_of_change + stat.pstdev(y_tmp),2),
            round(y_tmp[i] * rate_of_change - stat.pstdev(y_tmp),2)
        ]
        client.set(query, "true")
        client.set(f'{query}.upper',b[0])
        client.set(f'{query}.lower',b[1])
        print(f'Added {ticker} to db')
        return b
