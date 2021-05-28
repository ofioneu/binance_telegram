import flask
from flask import Flask
from flask_telegram.server import telegram_server
from trader.trader_server import trader_server


app = Flask(__name__)

app.register_blueprint(telegram_server)
app.register_blueprint(trader_server)



if __name__ == "__main__":
	app.run(debug=True)

