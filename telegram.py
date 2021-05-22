# -*- coding: utf-8 -*-
"""
This Example will show you how to use register_next_step handler.
"""
import telebot
import requests
import time
import configparser
import json

config = configparser.ConfigParser()

config.read('config.ini')


bot = telebot.TeleBot(config['DEFAULT']['token'])

url_price = 'http://127.0.0.1:5000/check_price' 
url_venda = 'http://127.0.0.1:5000/check_venda'
url_compra = 'http://127.0.0.1:5000/compra'


print('rodando...')

@bot.message_handler(commands=['vender'])
def send_welcome(message):
    try:
        response = requests.get(url_price)
        preco=response.json()
        new_preco = preco['price']
        msg = bot.reply_to(message, """\
            Seja bem vindo!
            O valor atual de venda do BTC é: {}
            Qual o valor de venda?
            """.format(new_preco))
        bot.register_next_step_handler(msg, venda)
    except Exception as e:
        bot.reply_to(message, 'Comando não reconhecido! : {}'.format(e))
        print(e)


def venda(message):
    try:
        preco_msg = message.text
        if not preco_msg.isdigit():
            msg = bot.reply_to(message, 'O preço precisa ser um numero. Qual o valor de venda? Ou Digite Retornar para reiniciar.')
            if preco_msg == 'Retornar':
                bot.register_next_step_handler(msg, send_welcome)
                return           
            elif preco_msg != 'Retornar':
                bot.register_next_step_handler(msg, venda)
                return
            return
        preco = {'preco':preco_msg}
        preco_json =  json.dumps(preco)
        msg = bot.reply_to(message, 'Ok! avisaremos quando esse preço chegar!')
        requests.post(url_venda, data = preco_json)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'oooops')
# **********************************************************************
#Compras

@bot.message_handler(commands=['comprar'])
def send_welcome_compra(message):
    try:
        response = requests.get(url_price)
        preco=response.json()
        new_preco = preco['price']
        msg = bot.reply_to(message, """\
            Seja bem vindo!
            O valor atual da compra do BTC é: {}
            Qual o valor de compra?
            """.format(new_preco))
        bot.register_next_step_handler(msg, venda)
    except Exception as e:
        bot.reply_to(message, 'Comando não reconhecido! : {}'.format(e))
        print(e)


def comprar(message):
    try:
        preco_msg = message.text
        if not preco_msg.isdigit():
            msg = bot.reply_to(message, 'O preço precisa ser um numero. Qual o valor de venda? Ou Digite Retornar para reiniciar.')
            if preco_msg == 'Retornar':
                bot.register_next_step_handler(msg, send_welcome_compra)
                return           
            elif preco_msg != 'Retornar':
                bot.register_next_step_handler(msg, comprar)
                return
            return
        preco = {'preco':preco_msg}
        preco_json =  json.dumps(preco)
        msg = bot.reply_to(message, 'Ok! avisaremos quando esse preço chegar!')
        requests.post(url_compra, data = preco_json)
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