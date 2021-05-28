from os import kill
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


klines = client.get_historical_klines("ETHBRL", Client.KLINE_INTERVAL_1DAY, "14 day ago UTC")
opened=[]
closed=[]
def abre(target,result):
    return result.append(target[1])

def fecha(target,result):
    return result.append(target[4])

for i in klines:
    abre(i,opened)
    
for i in klines:
    fecha(i,closed)

diff_result = [float(x1) - float(x2) for (x1, x2) in zip(closed, opened)]

vp = []
vn =[]

for i in diff_result:
    if i < 0:
        vn.append(i)
    else:
        vp.append(i)

def mid(vet):
    return sum(vet)/len(vet)

mid_vp = mid(vp)
mid_vn = mid(vn)

fr = mid_vp/abs(mid_vn)

rsi = 100 -(100/(1+fr))

print('FR= ',fr)
print('RSI= ',rsi)





