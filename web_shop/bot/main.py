from telebot import TeleBot
from .config import TOKEN
from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    Update
)

from .keyboards import START_KB
from flask import Flask
from flask import request, abort

bot = TeleBot(TOKEN)
app = Flask(__name__)


@app.route('/', methods=['POST'])
def process_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(status=403)

def set_webhook():
    import time

    bot.remove_webhook()
    time.sleep(2)
    bot.set_webhook(
        url='https://35.246.165.155/consecrate',
        certificate=open('web_shop/bot/webhook_cert.pem', 'r')
    )

@bot.message_handler(commands=['start'])
def start(message):
    kb = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    buttons = [KeyboardButton(value) for value in START_KB.values()]

    kb.add(*buttons)
    print(message)

    bot.send_message(
        message.chat.id,
        'Привет! Че делать будем?',
        reply_markup=kb
    )

@bot.message_handler(func=lambda message: message.text == START_KB['consecrate'], content_types=['text'])
def categories_handler(message):
    bot.send_message(
        message.chat.id,
        "Пришли мне фоточку того, что святить будешь"
    )

@bot.message_handler(func=lambda message: message.text == START_KB['forgive_sins'], content_types=['text'])
def categories_handler(message):
    bot.send_message(
        message.chat.id,
        "Отпущено, грешничек"
    )

@bot.message_handler(content_types=['text'])
def categories_handler(message):
    bot.send_message(
        message.chat.id,
        "Чет не понятно. может на /start ?"
    )

@bot.message_handler(content_types=['photo'])
def categories_handler(message):

    with open('photo_2020-04-17_20-53-28.jpg', 'rb') as file:
        bot.send_photo(
            chat_id=message.chat.id,
            photo=file,
            disable_notification=True
        )
