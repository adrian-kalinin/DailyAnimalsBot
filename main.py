from flask import Flask, request, jsonify
from flask_sslify import SSLify
import requests
import telebot
import json
import pickle


app = Flask(__name__)
sslify = SSLify(app)

token = 'token_from_botfather'
bot = telebot.TeleBot(token)

admin = 291702642
stat = {'cats': 0, 'dogs' : 0}
users = set()


def load_data():
    global stat, users
    with open('stat.json', 'r', encoding='utf-8') as file:
        stat.update(json.load(file))
    with open('users.bin', 'rb') as file:
        users = pickle.load(file)

def save_data():
    global stat, users
    with open('stat.json', 'w', encoding='utf-8') as file:
        json.dump(stat, file)
    with open('users.bin', 'wb') as file:
        pickle.dump(users, file)
    bot.send_message(admin, 'Данные успешно сохранены.')


@bot.message_handler(commands=['start'])
def handle_start(message):
    global users
    if not message.chat.id in users: users.add(message.chat.id)
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Получить котика :3')
    user_markup.row('Предпочитаю пёсиков!')
    bot.send_message(message.chat.id, 'Приветики, спасибо за использования бота :3 \
                                       @tweather_bot - основной проект.', reply_markup=user_markup)


@bot.message_handler(commands=['stat'])
def handle_stat(message):
    global stat, users, admin
    if message.chat.id == admin:
        bot.send_message(message.chat.id, f'{len(users)} users.\n{stat["cats"]} cats.\n{stat["dogs"]} dogs.')


@bot.message_handler(commands=['users'])
def handle_users(message):
    global users, admin
    if message.chat.id == admin:
        text = ''
        for user in users:
            text += str(user) + ' '
        bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['save'])
def handle_save(message):
    save_data()


@bot.message_handler(content_types=['text'])
def handle_picture(message):
    global stat
    if message.text == 'Получить котика :3' or message.text == '/cat' or message.text == '/cat@CasualCatsBot':
        cat = requests.get('https://api.thecatapi.com/v1/images/search').json()[0]['url']
        bot.send_photo(message.chat.id, requests.get(cat).content)
        stat['cats'] += 1

    elif message.text == 'Предпочитаю пёсиков!' or message.text == '/dog' or message.text == '/dog@CasualCatsBot':
        dog = requests.get('https://api.thecatapi.com/v1/images/search').json()[0]['url']
        bot.send_photo(message.chat.id, requests.get(dog).content)
        stat['dogs'] += 1


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()

        update = telebot.types.Update.de_json(r)
        bot.process_new_updates([update])

        return jsonify(r)
    return '<link rel="icon" href="data:;base64,=">'


if __name__ == '__main__':
    load_data()
    bot.remove_webhook()
    bot.set_webhook('your_webhook_url')
    app.run(host='0.0.0.0', port=8080)