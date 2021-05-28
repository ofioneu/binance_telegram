from flask import Flask, request
from flask.helpers import stream_with_context
import requests
import json
import telebot
import configparser
import sqlite3
from flask import Blueprint

telegram_server = Blueprint('telegram_server', __name__)

config = configparser.ConfigParser()

config.read('config.ini')


bot = telebot.TeleBot(config['DEFAULT']['token'])
chat_id = config['DEFAULT']['chat_id']

conn = sqlite3.connect('cripto.db', check_same_thread= False)
cur =conn.cursor()

url_binace = 'https://api.binance.com/api/v3/ticker/price?symbol='
url_check_price = 'http://127.0.0.1:5000/check_price_btc' 

@telegram_server.route('/moeda/<string:moeda>', methods=['POST', 'GET'])
def moeda(moeda):
    try:
        with open('moeda.txt', 'w') as moeda_:
            moeda_.write(moeda)
        return moeda
    except Exception as e:
        print('Não foi possivel gravar a moeda no arquivo txt!  :', e)

#Função que checa o preço na binance e retorna o preço
@telegram_server.route('/check_price_btc/<string:moeda>', methods = ['GET', 'POST'])
def check_price_btc(moeda):
    response = requests.get(url_binace+moeda.upper()+'BRL') #Faz uma requisição na binance da moeda enviada
    new_preco = response.json() #converte em json
    preco=new_preco['price'] #atribui o valor do preço
    data= {'price': preco} #cria um dict com o preço
    data_json = json.dumps(data) # converte em json
    return data_json #retorna o json


#função que registra a intenção de venda
@telegram_server.route("/register", methods=['POST'])
def register():
    data=request.get_json(force=True) #recebe do telegra a intenção de preço de venda
    lucro = data['lucro']
    with open('moeda.txt', 'r') as moeda_:
        moeda = moeda_.read()
    
    cur.execute("update ganho set {} = {}".format(moeda, lucro))
    conn.commit()
    conn.close()
    
    return ''
    
'''if __name__ == "__main__":
	app.run(debug=True)'''

