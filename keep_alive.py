import flask
from flask import Flask
from threading import Thread
import telebot.types
app = Flask(__name__)

@app.route('/')
def home():
    return "OK!"
@app.route('/', methods=['POST'])
def webhook(bot):
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()