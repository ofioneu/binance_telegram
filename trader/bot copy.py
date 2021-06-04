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
from datetime import datetime
import logging
#from logging.config import fileConfig

#fileConfig('../log/logging.cfg')
print("rodando bot...")

logging.basicConfig(filename='../log/bot.log', encoding='utf-8', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')

logging.info('TraderBot iniciado!')

config = configparser.ConfigParser()
config.read('C:/Users/HP/Desktop/Dev/Binance_telegran/config.ini')

api_key = config['BINACE_API']['api_key']
api_secret = config['BINACE_API']['secret_key']

client = Client(api_key, api_secret)

url_get_register_comand_bot ='http://127.0.0.1:5000//trader_server/get_register_comand_bot/'
url_get_register_coin ='http://127.0.0.1:5000//trader_server/get_register_coin/'
url_moeda = 'http://127.0.0.1:5000//trader_server/moeda/'
url_indicador = 'http://127.0.0.1:5000//trader_server/indicador/'

def main():
    pass

try:
    while True:
        flag_cmd_res =  requests.get(url_get_register_comand_bot) #bool true para iniciar bot ou false para não iniciar
        flag_cmd = flag_cmd_res.json() # var flag_cmd = comand bot
        status_bot = flag_cmd['flag_cmd'] #status oparacional do bot
        
        flag_moeda_res = requests.get(url_get_register_coin) # to get moeda em questão
        flag_moeda = flag_moeda_res.json() # var moeda em questão

        print('Status bot: {}'.format(status_bot)) # imprime o status do robô, se ele tem permissão para operar      
        
        while status_bot == 'true':
            try:
                with open('kdj_flag.txt', 'r') as kdj_signal:
                    kdj_flag = kdj_signal.read() # pega o valor da flak kdj pra saber kdj é zero
                    

                indicador_rsi = requests.get(url_indicador) # to get insdicador rsi
                rsi = indicador_rsi.json() # var rsi

                indicador_kdj = requests.get(url_indicador+'kdj/'+'False') #to get indicador kdj + kdj tendendo a zero
                kdj = indicador_kdj.json() #var kdj

                #kdj_backtrack = requests.get(url_indicador+'kdj/'+'True') #kdj com um periodo pra traz
                #backtrack = kdj_backtrack.json() # var kdj backtrack

                k= round(kdj['kdj_var']['valueK'],2)
                d=round(kdj['kdj_var']['valueD'],2)
                j=round(kdj['kdj_var']['valueJ'],2)
                kdj_zero = kdj['kdj_zero']    
                    
                print('KDJ: K:{}, D:{}, J:{} --- kdj_zero: {}'.format(k,d,j, kdj_zero))
                print('RSI: ', rsi)

#______________________ Registra o entrucamento do KDJ no ponto 0 _______________________
                    
                if kdj_zero == 0:
                    logging.info('Kdj convergiu a 0')
                    
                    with open('kdj_flag.txt', 'w') as kdj_flag:                            
                        kdj_flag.writelines('True')

#_________________________________ Comeca o a analise ___________________________________   

                with open('kdj_flag.txt', 'r') as kdj_file:
                    kdj_valor_true = kdj_file.read()
                    
                    
                if rsi < 30 and kdj_valor_true == 'True':
                    logging.info('RSI < 30 E kdj_valor_true == True')
                    kdj_backtrack=requests.get(url_indicador+'kdj/'+'True')

                    backtrack = kdj_backtrack.json()

                    kdj_var_backtrack = backtrack['kdj_var']

                    k_backtrack=kdj_var_backtrack['valueK']
                    d_backtrack=kdj_var_backtrack['valueD']
                    j_backtrack=kdj_var_backtrack['valueJ']

                    if k_backtrack < d and k > d:
                        logging.info('k_backtrack < D E K > D')
                        res=requests.post(url_moeda+flag_moeda['flag_moeda'])
                        res_json = res.json()
                        print("compraria ao valor de: {}". format(res_json['price']))
                        with open('logTrader.txt', 'a') as log:
                            local_dt = datetime.now()                            
                            log.writelines("{} --Compraria ao valor de: {} em um RSI: {}\n". format(local_dt, res_json['price'], rsi))
                            
                        with open('kdj_flag.txt', 'w') as kdj_signal:
                            kdj_signal.write('False')
                            logging.info('Setou o valor de kdj_flag.txt para False')
                    
                if rsi > 80 and kdj_valor_true == 'True':
                    logging.info('RSI > 80 E kdj_valor_true == True')
                    kdj_backtrack=requests.get(url_indicador+'kdj/'+'True')
                    backtrack = kdj_backtrack.json()

                    kdj_var_backtrack = backtrack['kdj_var']

                    k_backtrack=kdj_var_backtrack['valueK']
                    d_backtrack=kdj_var_backtrack['valueD']
                    j_backtrack=kdj_var_backtrack['valueJ']                   
                        
                    if k_backtrack > d and k < d:
                        logging.info('k_backtrack > D E K < D')
                        res=requests.post(url_moeda+flag_moeda['flag_moeda'])
                        res_json = res.json()
                        print("venderia ao valor de: {}". format(res_json['price']))
                        with open('logTrader.txt', 'a') as log:
                            local_dt = datetime.now()                            
                            log.writelines("{} --Venderia ao valor de: {} em um RSI: {}\n". format(local_dt, res_json['price'], rsi))
                        with open('kdj_flag.txt', 'w') as kdj_signal:
                            kdj_signal.write('False')
                            logging.info('Setou o valor de kdj_flag.txt para False')
                        
                time.sleep(5)
            except Exception as e:
                logging.warning('Opps!: %s', e)
                print("Opss!: %s", e)
        time.sleep(10)
except Exception as e:
    logging.warning('Opps!: %s', e)



            
