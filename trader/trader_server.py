#from flask import Flask, request, Blueprint
#from flask.helpers import stream_with_context
import requests
import sqlite3
import asyncio
import configparser
from binance.enums import *
from binance import AsyncClient
import json

config = configparser.ConfigParser()
config.read('C:/Users/HP/Desktop/Dev/Binance_telegran/config.ini')

api_key = config['BINACE_API']['api_key']
api_secret = config['BINACE_API']['secret_key']

#trader_server = Blueprint('trader_server', __name__)

async def teste(client):
    info = await client.get_account()
    print(json.dumps(info, indent= 2))

#função que pegará o retorno dos modulos do trader e salvar no banco para outra função fazer os cauculos
'''@trader_server.route('/trader_server', methods=['GET', 'POST'])
def trader_server():
    pass'''


async def main():
    client = await AsyncClient.create()  
    #a= await client.ping()

    #await teste(client) #ok
    #status = await client.get_account_status() # funciona no arquivo teste, é sincrono
    #tickers = await client.get_ticker() #0k
    #time_res = await client.get_server_time() #ok
    #status = await client.get_system_status()# ok
    #info =  await client.get_exchange_info()#ok
    #info = await client.get_symbol_info('ETHBRL')#ok
    info = await client.get_all_tickers(symbol='ETHBRL') #ok, vou usar retorna uma lista// traz o preco atual da moeda
    #info = client.get_account_snapshot(type='SPOT')
    #products =  await client.get_products() #ok
    #depth = await client.get_order_book(symbol='BTCBRL')#ok, posso usar no futuro
    #trades = await client.get_recent_trades(symbol='BTCBRL') #ok
    #avg_price = await client.get_avg_price(symbol='ETHBRL') #ok

    #info = await client.get_account()
    #print(info)
    

    print(json.dumps(info, indent= 2))
    

    await client.close_connection()

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


    
    
  


#print(order(symbol, side, type, timeInForce, quantity, price))
    



    