from flask import Flask, request, jsonify
import requests
from flask_sslify import SSLify
import json
import pickle

app = Flask(__name__)
sslify = SSLify(app)

token = ''
admin = 291702642
users = set()

stat = {'cats': 0}
users = set()


def load_data():
    global stat, users
    try:
        with open('stat.json', 'r', encoding='utf-8') as file: 
            stat = json.load(file)
        with open('users.bin', 'rb') as file:
            users = pickle.load(file)
    except:
        pass

def save_data(chat_id):
    global stat, users

    with open('stat.json', 'w', encoding='utf-8') as file:
        json.dump(stat, file)
    with open('users.bin', 'wb') as file:
        pickle.dump(users, file)
    text = 'Данные успешно сохранены.'
    send_message(chat_id, text)
                  
def send_message(chat_id, text, buttons=[['Получить котика!']]):
    global token
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    keyboard = {'keyboard': buttons, 'resize_keyboard': True}
    answer = {'chat_id': chat_id, 'text': text, 'reply_markup': keyboard}
    requests.post(url, json=answer)

def send_cat(chat_id):
    global token
    cat = requests.get('https://api.thecatapi.com/v1/images/search?api_key=ccdeda03-f77a-4657-9d3a-7468a50ea9e8').json()[0]['url']
    url = f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}&photo={cat}'
    requests.get(url)
    global stat
    stat['cats'] += 1

def get_data(r):
        if 'message' in r:
            if 'text' in r['message']:
                data = {'chat_id': r['message']['chat']['id'],
                        'text': r['message']['text'],
                        'type': r['message']['chat']['type']}

                global users
                if data['type'] == 'private' and data['chat_id'] not in users: users.add(data['chat_id'])

                return data
        else:
            return None

admin_commands = {'/save': save_data}

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        data = get_data(r)

        global admin, stat, users
        text = ''

        if not data == None:
            if data['text'] == '/start':
                text = 'Приветики, спасибо за использования бота :3'
                send_message(data['chat_id'], text)

            elif data['text'] == '/cat' or data['text'] == 'Получить котика!' or data['text'] == '/cat@CasualCatsBot':
                send_cat(data['chat_id'])

            elif data['text'] == '/stat' and data['chat_id'] == admin:
                text = f'{stat["cats"]} cats.\n{len(users)}'
                send_message(data['chat_id'], text)

            elif data['text'] == '/users' and data['chat_id'] == admin:
                for user in users:
                    text += str(user) + '\n'
                send_message(data['chat_id'], text)

            elif data['text'] == '/save' and data['chat_id'] == admin:
                save_data(data['chat_id'])

        return jsonify(r)
    return '<link rel="icon" href="data:;base64,=">'


if __name__ == '__main__':
    load_data()
    app.run(host='0.0.0.0', port=8080)