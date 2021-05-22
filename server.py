from os import close
from flask import Flask, request
import requests
import json
import telebot
import configparser
import sqlite3


app = Flask(__name__)

config = configparser.ConfigParser()

config.read('config.ini')


bot = telebot.TeleBot(config['DEFAULT']['token'])
chat_id = config['DEFAULT']['chat_id']

conn = sqlite3.connect('cripto.db')

url_binace = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCBRL'
url_check_price = 'http://127.0.0.1:5000/check_price' 

#Função que checa o preço na binance e retorna o preço
@app.route('/check_price', methods = ['GET'])
def check_price():
    response = requests.get(url_binace) #Faz uma requisição na binance
    new_preco = response.json() #converte em json
    preco=new_preco['price'] #atribui o valor do preço
    data= {'price': preco} #cria um dict com o preço
    data_json = json.dumps(data) # converte em json
    return data_json #retorna o json


#função que registra a intenção de venda
@app.route("/check_venda", methods=['POST'])
def check_venda():
    data=request.get_json(force=True) #recebe do telegra a intenção de preço de venda
    response = requests.get(url_check_price) #Recebe a res da rota /check_price
    res_json = response.json() #converte para json
    print('response: ',res_json)
    conn.execute("update precos set preco_venda = {}".format(data['preco']))
    conn.commit()
    conn;close()
    #Se o preço for maior ou igual ao preço intencional de venda ele reorna uma
    #mensagem para vender no telegram
    
    if res_json['price'] >= data['preco']:
        bot.send_message(chat_id,"Hora de vender! : R${}".format(res_json['price']))
    
    return res_json['price']
    
#********************************************************************************
#Comprar

#Função que registra intenção de compra
@app.route("/check_compra", methods=['POST'])
def check_compra():
    print('ok')
    data=request.get_json(force=True)
    print('data: ', data)
    response = requests.get(url_check_price)
    res_json = response.json()
    #Se o preço for maior ou igual ao preço intencional de venda ele reorna uma
    #mensagem para vender no telegram 
    if res_json['price'] <= data['preco']:
        bot.send_message(chat_id,"Hora de comprar! : {}".format(res_json['price']))
    
    return res_json['price']

if __name__ == "__main__":
	app.run(debug=True)

