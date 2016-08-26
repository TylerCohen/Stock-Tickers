from googlefinance import getQuotes
import json
import ast

##dictionary for tickers
tickers = ['AAPL', 'AMZN', 'DIS', 'FB', 'GOOGL', 'GS', 'HD', 'NFLX', 'NOC', 'TSLA']
shares = {'AAPL': 10, 'AMZN': 2, 'DIS': 10, 'FB': 10, 'GOOGL': 2, 'GS': 5, 'HD': 5, 'NFLX': 10, 'NOC': 5, 'TSLA': 5}
pricePaid = {'AAPL': 120.00, 'AMZN': 625, 'DIS': 100, 'FB': 94, 'GOOGL': 700, 'GS': 180, 'HD': 35, 'NFLX': 120, 'NOC': 217, 'TSLA': 200}

##creates dictionary to store last price
last = {}
gainloss = {}

##loops through tickers and updates 'last' dictionary with each ticker's last price
for ticker in tickers:
    stockInfo = json.dumps(getQuotes(ticker))   #pulls stock quote
    stockInfo = stockInfo[1:(len(stockInfo)-1)] #parses string
    stockInfo = ast.literal_eval(stockInfo)     #converts string into dictionary
    last[ticker] = stockInfo['LastTradePrice']
    gainloss[ticker] = ((float(stockInfo['LastTradePrice']))-(pricePaid[ticker]))*(float(shares[ticker]))

#sorts tickers alphabetically and prints
print('LAST PRICE:')
for keys,values in sorted(last.items()):
    print(keys,': ', values)
    
print('GAIN(LOSS):')
for keys,values in sorted(gainloss.items()):
    print(keys,': ', int(values))
print('TOTAL GAIN(LOSS): ', int(sum(gainloss.values())))
