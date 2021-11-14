import json
import pandas as pd
from robin_stocks import robinhood as rh
import auth

rh.authentication.login(auth.USERNAME, auth.PASSWORD)
f = open('stocks.json')
stocks = json.load(f)

for stock in stocks:
    print(rh.stocks.get_latest_price(stock["Symbol"])[0])
    rh.stocks.get_stock_historicals
