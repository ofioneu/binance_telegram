import configparser
import json
import requests

config = configparser.ConfigParser()

config.read('C:/Users/HP/Desktop/Dev/Binance_telegran/config.ini')

try:
    secret = (config['taapi_io']['secret_key'])
except Exception as e:
    print(e)


def kdj(moeda,interval, backtrack):
    endpoint= 'https://api.taapi.io/kdj'
    if backtrack == 'False':
        parameters = {
            'secret': secret,
            'exchange': 'binance',
            'symbol': moeda,
            'interval': interval,
            'period': 9,
            'signal': 3

        }
        # Send get request and save the response as response object 
        response = requests.get(url = endpoint, params = parameters)
        # Extract data in json format 
        result = response.json() 

        # Print result
        #print('RESULT: ',result)

        return result
    
    if backtrack == 'True':
        parameters = {
            'secret': secret,
            'exchange': 'binance',
            'symbol': moeda,
            'interval': interval,
            'period': 9,
            'signal': 3,
            'backtrack':1
        }
        # Send get request and save the response as response object 
        response = requests.get(url = endpoint, params = parameters)
        # Extract data in json format 
        result = response.json() 

        # Print result
        #print('RESULT: ',result)

        return result


  
    

#print('print:',kdj('ETH/BRL', '1h', False))