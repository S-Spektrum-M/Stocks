import json
import pandas as pd
from robin_stocks import robinhood as rh
import auth

rh.authentication.login(auth.USERNAME, auth.PASSWORD)
f = open('stocks.json')
stocks = json.load(f)

for stock in stocks:
    try:
        prices = rh.stocks.get_stock_historicals(stock["Symbol"])
        for price in prices:
            print(f'{stock["Symbol"]}: open: {price["open_price"]} close: {price["close_price"]}')
    except TypeError:
        print("Bad Entry")

f.close()
