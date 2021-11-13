import json
import pandas as pd
from robin_stocks import robinhood as rh
import auth

rh.authentication.login(auth.USERNAME, auth.PASSWORD)
