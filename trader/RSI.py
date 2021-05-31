import configparser
from binance.enums import *
from binance import Client
import datetime

config = configparser.ConfigParser()
config.read('C:/Users/HP/Desktop/Dev/Binance_telegran/config.ini')

api_key = config['BINACE_API']['api_key']
api_secret = config['BINACE_API']['secret_key']

client = Client(api_key, api_secret)

def rsi_return():
    with open('C:/Users/HP/Desktop/Dev/Binance_telegran/telegram/moeda.txt', 'r') as cmd_bot:
        moeda=cmd_bot.readline()       
    klines = client.get_historical_klines(moeda, Client.KLINE_INTERVAL_1HOUR, "14 day ago UTC")#precisa deixar a moeda editável aqui
    opened=[]
    closed=[]
    tamanho_klines = len(klines)
    time_mls = klines[tamanho_klines-1][0]
    time_date = datetime.datetime.fromtimestamp(time_mls/1000.0)
    print('time:',time_date)
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

    
    print('len_vp: ', len(vp))

    #***Não suavizado***
    '''mid_vp = mid(vp)
    mid_vn = mid(vn) 
    fr = mid_vp/abs(mid_vn)'''
    
    #_____Suavizado____
    len_vp = len(vp)
    len_vn = len(vn)
    mid_vp = mid(vp[0:12])
    mid_vn = mid(vn[0:12])
    mid_vp_down = ((mid_vp * 13)+vp[len_vp-1])/14
    mid_vn_down = ((mid_vn * 13)+vn[len_vn-1])/14
    fr = mid_vp_down/abs(mid_vn_down)

    
    

    rsi = 100 -(100/(1+fr))
    rsi_around = round(rsi, 2)

    return rsi_around





