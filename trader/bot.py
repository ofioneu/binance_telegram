#o bot tem que receber um comando para começar à trabalhar
#depois que ele estar ativado ele tera que checar os dados do rsi para saber 
# se está na hora de comprar ou vender e informar o telegram

#from trader.trader_server import indicador
import requests
import configparser
from binance.enums import *
from binance import Client
import json
#from RSI import rsi_return
import threading
import time


print("rodando bot...")
config = configparser.ConfigParser()
config.read('C:/Users/HP/Desktop/Dev/Binance_telegran/config.ini')

api_key = config['BINACE_API']['api_key']
api_secret = config['BINACE_API']['secret_key']

client = Client(api_key, api_secret)

url_get_register_comand_bot ='http://127.0.0.1:5000//trader_server/get_register_comand_bot/'
url_get_register_coin ='http://127.0.0.1:5000//trader_server/get_register_coin/'
url_moeda = 'http://127.0.0.1:5000//trader_server/moeda/'
url_indicador = 'http://127.0.0.1:5000//trader_server/indicador/'

while True:
    flag_cmd_res =  requests.get(url_get_register_comand_bot)
    flag_cmd = flag_cmd_res.json()
    flag_moeda_res = requests.get(url_get_register_coin)
    flag_moeda = flag_moeda_res.json()
    
    print('Flag cmd: ',flag_cmd)
    
    if flag_cmd['flag_cmd'] == 'true':
        while flag_cmd['flag_cmd'] == 'true':
            try:
                indicador = requests.get(url_indicador)
                indicador_json = indicador.json()
                flag_cmd_res =  requests.get(url_get_register_comand_bot)
                flag_cmd = flag_cmd_res.json()
                flag_moeda_res = requests.get(url_get_register_coin)
                flag_moeda = flag_moeda_res.json()
                #rsi = indicador_json['rsi']
                print(indicador_json)
            except Exception as e:
                print("Servidor OFFLINE: ", e)
        '''
            finally:
                #print('rsi: ', rsi)
                if rsi < 30:
                    res=requests.post(url_moeda+flag_moeda['flag_moeda'])
                    res_json = res.json()
                    print("compraria ao valor de: {}". format(res_json['price']))
                
                if rsi > 80:
                    res=requests.post(url_moeda+flag_moeda)
                    res_json = res.json()
                    print("compraria ao valor de: {}". format(res_json['price']))'''
    
        time.sleep(5)
    time.sleep(10)
            
