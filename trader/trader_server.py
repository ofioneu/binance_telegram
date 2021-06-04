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
import logging
#from logging.config import fileConfig
from trader.RSI import rsi_return
from trader.KDJ import kdj

#config
#fileConfig('./log/logging.cfg')#Le as configurações de log
log = logging.getLogger('werkzeug')
log.disabled = True

logging.basicConfig(filename='./log/trader_server.log', encoding='utf-8', level=logging.INFO)

config = configparser.ConfigParser()#le as configurações de API's
config.read('C:/Users/HP/Desktop/Dev/Binance_telegran/config.ini')
api_key = config['BINACE_API']['api_key']
api_secret = config['BINACE_API']['secret_key']


#blueprint
trader_server_blueprint = Blueprint('trader_server_blueprint', __name__)

#*********Rotas que retornam valores do trader ou da exchenge***************


logging.info('Trader server iniciado!')
@trader_server_blueprint.route('/', methods=['GET'])
def sinal():
    return '', 200

#retorna os valores dos indicadores
@trader_server_blueprint.route('/trader_server/indicador/', methods=['GET', 'POST'])
def indicador():
    try:
        rsi = rsi_return() 
        return json.dumps(rsi)
    except Exception as e:
        logging.error('Não foi possível receber as informaçoes de rsi da função rsi_retun: %s', e)

    

@trader_server_blueprint.route('/trader_server/indicador/kdj/<string:backtrack>', methods=['POST', 'GET'])
def indicador_kdj(backtrack):
    print('BACKTRACK STATUS: ', backtrack)
    try:
        with open('C:/Users/HP/Desktop/Dev/Binance_telegran/telegram/moeda.txt', 'r') as cmd_bot:
                flag_moeda=cmd_bot.readline()
                moeda = flag_moeda.replace('BRL','/BRL')
    
        print('MOEDA: ', moeda)
        kdj_var = kdj(moeda,'1h', backtrack)
    
        def kdj_diff(n1,n2,n3):
            vet = [n1, n2, n3]
            vet.sort(reverse=True)
            #print('vet: ', vet)
            r1 = vet[0] - vet[1]
            r2= vet[0] - vet[2]
            r3= r1 + r2
            return round(r3, 2)
        
        kdj_zero = kdj_diff(kdj_var['valueK'], kdj_var['valueD'], kdj_var['valueJ'])
        data={
            'kdj_var' : kdj_var,
            'kdj_zero': kdj_zero
            }          
        return json.dumps(data)
    except Exception as e:
        logging.error('Não foi possível enviar as informaçoes solicitadas: %s', e)





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



    
