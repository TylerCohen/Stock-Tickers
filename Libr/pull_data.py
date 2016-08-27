import json
import ast
import time
from .googlefinance import getQuotes


##loops through tickers and updates 'last' dictionary with each ticker's last price
def last_price(*args):
    if len(args) == 1:
        stockinfo = json.dumps(getQuotes(args))
        stockinfo = ast.literal_eval(stockinfo)
        stockinfo = stockinfo[0]
        last_price = stockinfo['LastTradePrice']
        return last_price
    last_price = {}
    for ticker in args:
        stockinfo = json.dumps(getQuotes(ticker))   #pulls stock quote
        stockinfo = stockinfo[1:(len(stockinfo)-1)] #parses string
        stockinfo = ast.literal_eval(stockinfo)     #converts string into dictionary
        last_price[ticker] = float(stockinfo['LastTradePrice'])
    return last_price

if __name__ == '__main__':
    print(last_price('aapl', 'msft'))