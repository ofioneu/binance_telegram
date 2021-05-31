# -*- coding: utf-8 -*-
import telebot
import requests
import time
import configparser
import json
#from telegram.register_step
from telebot.types import Message, Update

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
url_moeda = 'http://127.0.0.1:5000//trader_server/moeda/'
url_account = 'http://127.0.0.1:5000/trader_server/account/'
url_klines = 'http://127.0.0.1:5000/trader_server/klines/'


print('rodando...')

@bot.message_handler(commands=['help'])
def send_welcome_help(message):
    try:
        bot.send_message(chat_id, """Seja bem vindo!
        lista de comandos:
        1- /price: retorna o preço atual da moeda
        2- /conta: retorna um snapshot da sua conta
        3- /klines: retorna oas informações de uma vela especifica em um determinado periodo(comando ainda não desenvolvido)
        4 - /coinbot: inicia uma conversa com o robo trader
        """)
    except Exception as e:
        bot.reply_to(message,'Comando não reconhecido! : {}'.format(e))
        print(e)

@bot.message_handler(commands=['coinbot'])
def send_welcome_bot(message):
    try:
        res = requests.get(url_account)
        res_data = res.json()
        msg = bot.reply_to(message, """Olá eu sou o Coinbot!
        Vou te dar algumas informações da sua conta:
        {}.
        Digite "yes" para começar ou digite "no" para sair.          
        """.format(res_data))
        
        
        bot.register_next_step_handler(msg, next_step_coinbot)
    except Exception as e:
        bot.reply_to(message, 'Comando não reconhecido! : {}'.format(e))
        print(e)

def next_step_coinbot(message):
    try:
        print('texto_msg: ', message.text)
        if message.text == 'yes':
            msg = bot.reply_to(message, """
            Ok, então sem mais delongas, vamos começar!
            Qual a moeda que queres trabalhar?
            """)
            with open('comand_bot.txt', 'w') as cmd_bot:
                cmd_bot.writelines('true')
            bot.register_next_step_handler(msg, register_coin)
        elif message.text == 'no':
            with open('comand_bot.txt', 'w') as cmd_bot:
                cmd_bot.writelines('false')
                bot.send_message(chat_id, "Ok, Encerramos então..")        
    
    except Exception as e:
        bot.reply_to(message, 'Comando não reconhecido! : {}'.format(e))
        print(e)


def register_coin(message):
    try:
        msg = bot.reply_to(message, """
        Ok, qual é a opeação que deseja trabalhar?
        Digite "venda" para vender ou "compra" para comprar
        """)
        m=message.text.upper()
        with open('moeda.txt', 'w') as cmd_bot:
            cmd_bot.writelines(m)
        
        bot.register_next_step_handler(msg, register_operation)
    
    except Exception as e:
        bot.reply_to(message, 'Comando não reconhecido! : {}'.format(e))
        print(e)

def register_operation(message):
    try:
        msg= message.text
        with open('operation.txt', 'w') as cmd_bot:
            cmd_bot.writelines(msg)
            bot.send_message(chat_id,"""Ok! Registrado e Operando!""")
    except Exception as e:
        bot.reply_to(message, 'Comando não reconhecido! : {}'.format(e))
        print(e)

  

@bot.message_handler(commands=['price'])
def send_welcome_moeda(message):
    try:
        msg = bot.reply_to(message, """Seja bem vindo!
        De qual moeda deseja informações?      
        """)
        bot.register_next_step_handler(msg, moeda_price)
    except:
        bot.reply_to(message, 'Comando não reconhecido! : {}'.format(e))
        print(e)

def moeda_price(message):
    msg = message.text.lower()
    moeda_info_post = requests.post(url_moeda + msg)
    moeda_json = moeda_info_post.json()
    bot.send_message(chat_id, '''Aqui estão as informações solicitadas: 
    Symbol: {},
    Price: {}
    '''.format( moeda_json['symbol'], moeda_json['price']))


@bot.message_handler(commands=['conta'])
def send_welcome_accont(message):
    try:
        res = requests.get(url_account)
        res_data = res.json()
        msg = bot.reply_to(message, '''
        Seja bem vindo!
        Aqui está: 
        {}
        '''.format(res_data))
    except Exception as e:
        bot.reply_to(message, 'Comando não reconhecido! : {}'.format(e))
        print(e)


"""
@bot.message_handler(commands=['velas'])
def send_welcome_klines(message):
    try:
        msg = bot.reply_to(message, '''
        Seja bem vindo!
        Escolha uma moeda
        ''')
        bot.register_next_step_handler(msg, klines_moeda)
    except Exception as e:
        bot.reply_to(message, 'Comando não reconhecido! : {}'.format(e))
        print(e)

def klines_moeda(message):
    try:
        msg = bot.reply_to(message, '''
            Qual o periodo?

            ''')
        bot.register_next_step_handler(msg, klines_moeda)
    except Exception as e:
        bot.reply_to(message, 'Comando não reconhecido! : {}'.format(e))
        print(e)



def klines(message):
    msg = message.text.lower()
    klines_info_post = requests.post(url_klines + msg)
    klines_data = klines_info_post.json()
    bot.send_message(chat_id, '''Aqui estão as informações solicitadas: 
    {}
    '''.format(klines_data))    
"""

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


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)


# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.polling(interval=3)