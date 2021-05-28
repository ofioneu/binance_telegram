import requests
import sqlite3
import asyncio
import configparser
from binance.enums import *
from binance import Client
import json

config = configparser.ConfigParser()
config.read('C:/Users/HP/Desktop/Dev/Binance_telegran/config.ini')

api_key = config['BINACE_API']['api_key']
api_secret = config['BINACE_API']['secret_key']

client = Client(api_key, api_secret)

#status = client.get_account_status() # ok
'''
agg_trades = client.aggregate_trade_iter(symbol='ETHBTC', start_str= '1 hour ago UTC')
agg_trade_list = list(agg_trades)''' # Ok

#info = client.get_account_snapshot(type='SPOT') # ok
#info =  client.get_account() #ok
#status = client.get_account_status() #ok
#balance = client.get_asset_balance(asset='ETH')#ok
klines = client.get_historical_klines("ETHBRL", Client.KLINE_INTERVAL_1DAY, "14 day ago UTC")
print(klines)
'''a= klines[0][1]
b= klines[0][4]

c= float(b)-float(a)
print('A diferenca foi de: ', c)'''