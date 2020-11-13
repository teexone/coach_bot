from flask import Flask, request
from telegram import Bot, Update

import os

bot_token = os.environ['TELEGRAMAPI']
heroku_url = os.environ['HEROKUURL']
bot = Bot(bot_token)
app = Flask(__name__)


@app.route('/{}'.format(bot_token), methods=['POST'])
def respond():
    update = Update.de_json(request.get_json(force=True), bot)
    chat = update.message.chat.id
    message = update.message
    bot.send_message(chat, 'Working')


@app.route('/setwebhook', methods=['GET', 'POST'])
def hook():
    _set = bot.setWebhook('{URL}{HOOK}'.format(URL=heroku_url, HOOK=bot_token))
    if _set:
        print("Webhook has been established")
    else:
        print("Webhook establishment failed")
    return 'ok'

@app.route('/')
def index():
    return '<a href="http://github.com/teexone">Github Link</a>'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', threaded=True, port=port)
