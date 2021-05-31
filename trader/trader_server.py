from flask import Flask, request, Blueprint
#from flask.helpers import stream_with_context
import requests
import sqlite3
import asyncio
import configparser
from binance.enums import *
from binance import AsyncClient
from binance import Client
import json
from trader.RSI import rsi_return
from trader.KDJ import kdj

#config
config = configparser.ConfigParser()
config.read('C:/Users/HP/Desktop/Dev/Binance_telegran/config.ini')
api_key = config['BINACE_API']['api_key']
api_secret = config['BINACE_API']['secret_key']


#blueprint
trader_server_blueprint = Blueprint('trader_server_blueprint', __name__)

#*********Rotas que retornam valores do trader ou da exchenge***************

#retorna os valores dos indicadores
@trader_server_blueprint.route('/trader_server/indicador/', methods=['GET', 'POST'])
def indicador():
    with open('C:/Users/HP/Desktop/Dev/Binance_telegran/telegram/moeda.txt', 'r') as cmd_bot:
            flag_moeda=cmd_bot.readline()
            moeda = flag_moeda.replace('BRL','/BRL')
    rsi = rsi_return()
    kdj_var = kdj(moeda,'1h')
    data={
        "rsi": rsi,
        'kdj_var' : kdj_var
        }          
    return json.dumps(data)

#_______________________________________________________________________________________________

#Retona o valor atual da moeda
@trader_server_blueprint.route('/trader_server/moeda/<string:param>', methods=['GET', 'POST'])
async def moeda_price(param):
    moeda =  param.upper()
    print(moeda)
    client = await AsyncClient.create(api_key, api_secret)
    info = await client.get_all_tickers(symbol=str(moeda))
    print(info)
    await client.close_connection()
    return info


#retona um snapshot da conta
@trader_server_blueprint.route('/trader_server/account/', methods=['GET', 'POST'])
def account():
    client = Client(api_key, api_secret)
    info = client.get_account_snapshot(type='SPOT')
    info_data = json.dumps(info['snapshotVos'][1])
    print(info_data)
    return info_data
    

#retona um snapshot da as klines(falta desensvolver)
@trader_server_blueprint.route('/trader_server/klines/<moeda>/<period>', methods=['GET', 'POST'])
def klines(moeda,period):
    print(moeda, period)
    '''client = Client(api_key, api_secret)
    klines = client.get_historical_klines("ETHBRL", Client.KLINE_INTERVAL_1DAY, "14 day ago UTC")
    info_data = json.dumps(info['snapshotVos'][1])
    print(info_data)
    return info_data'''


@trader_server_blueprint.route('/trader_server/get_register_coin/', methods=['GET', 'POST'])
def get_register_coin():
    with open('C:/Users/HP/Desktop/Dev/Binance_telegran/telegram/moeda.txt', 'r') as cmd_bot:
        flag_moeda=cmd_bot.readline()
        print('flag_moeda', flag_moeda)
        response = {"flag_moeda": flag_moeda}
    return json.dumps(response)

@trader_server_blueprint.route('/trader_server/get_register_comand_bot/', methods=['GET', 'POST'])
def get_register_comand_bot():
    with open('C:/Users/HP/Desktop/Dev/Binance_telegran/telegram/comand_bot.txt', 'r') as cmd_bot:
        flag_cmd=cmd_bot.readline()
        print('falg_cmd: ', flag_cmd)
        response = {"flag_cmd": flag_cmd}
    return  json.dumps(response)
    

'''@trader_server_blueprint.route('/trader_server/klines/', methods=['GET', 'POST'])
def get_register_comand_bot():

    print('falg_cmd: ', flag_cmd)
    response = {"flag_cmd": flag_cmd}
    return json.dumps(response)'''



    
