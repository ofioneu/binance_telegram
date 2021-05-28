# -*- coding: utf-8 -*-

from requests.api import request
import telebot
import requests
import time
import configparser
import json
from register_step import register_step
from telebot.types import Update

config = configparser.ConfigParser()

config.read('C:/Users/HP/Desktop/Dev/Binance_telegran/config.ini')


try:
    bot = telebot.TeleBot(config['DEFAULT']['token'])
    chat_id = config['DEFAULT']['chat_id']
except Exception as e:
    print(e)

url_price = 'http://127.0.0.1:5000/check_price_btc/' 
url_register = 'http://127.0.0.1:5000/register'
url_compra = 'http://127.0.0.1:5000/check_compra_btc'
url_moeda = 'http://127.0.0.1:5000/moeda/'


print('rodando...')

def get_price(symbol):
    response = requests.get(url_price+symbol)
    preco=response.json()
    new_preco = preco['price']
    return new_preco


@bot.message_handler(commands=['trader'])
def send_welcome(message):
    try:
        msg = bot.reply_to(message, """\
            Seja bem vindo!
            Qual a moeda?
            """)
        bot.register_next_step_handler(msg, lucro)
    except Exception as e:
        bot.reply_to(message, 'Comando não reconhecido! : {}'.format(e))
        print(e)


def lucro(message):
    try:
        msg = message.text.lower()
        requests.post(url_moeda + msg)
        price = get_price(msg)
        msg = bot.reply_to(message, """\
        O valor da moeda agora é:{}
        Por favor digite a margem de lucro:
        """.format(price))
        bot.register_next_step_handler(msg, register)

        register_step(message, msg, url_register)

    except Exception as e:
        print(e)
        bot.reply_to(message, e)

def register(message):
    lucro = message.text.lower()
    try:
        data = {'lucro':lucro}
        data_json = json.dumps(data)
        requests.post(url_register, data= data_json)

        bot.send_message(chat_id, 'Ok, registrado!')    
    
    except Exception as e:
        print(e)
        bot.reply_to(message, e)

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)


# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.polling(interval=3)