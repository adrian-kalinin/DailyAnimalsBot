from pip._internal.utils import logging

from database import DBHelper, StatCounter
import requests
import telebot
import cherrypy
import config
import time

bot = telebot.TeleBot(config.token)
sc = StatCounter()


@bot.message_handler(commands=['start', 'start@CasualCatsBot'])
def handle_start(message):
    with DBHelper() as db:
        if not db.check_user(message.chat.id):
            db.add_user(message.chat.id)

    if message.chat.id > 0:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Получить котика :3')
        user_markup.row('Предпочитаю пёсиков!')

    text = 'Приветики, спасибо за использования бота :3'
    bot.send_message(message.chat.id, text, reply_markup=user_markup)


@bot.message_handler(commands=['stat'])
def handle_stat(message):
    with DBHelper() as db:
        users = db.get_users()
        text = f'{len(users)} users.\n{sc.cats} cats.\n{sc.dogs} dogs.'
        sc.save_data()
        bot.send_message(message.chat.id, text)


def check_mass(msg):
    return msg.from_user.id in config.admins and (msg.text and'/mass' in msg.text or msg.caption and '/mass' in msg.caption)


@bot.message_handler(func=check_mass)
def handle_mass_mailing(message):
    succesful, failed = mass_mailing(message)
    text = (f'Message has been sent to {succesful} users.\n! {failed} users were deleted.')
    bot.send_message(message.chat.id, text)


def mass_mailing(message):
    if msg.text:
        text = message.text.replace('/mass ', '')
    else:
        text = message.caption.replace('/mass ', '')
    with DBHelper() as db:
        users = db.get_users()
        succesful, failed = 0, 0

        for user in users:
            try:
                if message.photo:
                    bot.send_photo(user, message.photo, caption=text)
                else:
                    bot.send_message(user, text)
                succesful += 1
                time.sleep(1 / 30)

            except telebot.apihelper.ApiException:
                db.del_user(user)
                failed += 1

        return succesful, failed


@bot.message_handler(content_types=['text'])
def handle_picture(message):
    if message.text in ('Получить котика :3', '/cat', '/cat@CasualCatsBot'):
        data = requests.get('https://api.thecatapi.com/v1/images/search').json()
        bot.send_photo(message.chat.id, requests.get(data[0]['url']).content)
        sc.append_cat()

    elif message.text in ('Предпочитаю пёсиков!', '/dog', '/dog@CasualCatsBot'):
        data = requests.get('https://api.thedogapi.com/v1/images/search').json()
        bot.send_photo(message.chat.id, requests.get(data[0]['url']).content)
        sc.append_dog()


@bot.inline_handler(lambda query: query.query == 'cat')
def query_photo(inline_query):
    results = set()
    while len(results) < 8:
        url = requests.get('https://api.thecatapi.com/v1/images/search').json()[0]['url']
        results.add(telebot.types.InlineQueryResultPhoto(f'cat{len(results)}', url, url))
    bot.answer_inline_query(inline_query.id, results, cache_time=1)


@bot.inline_handler(lambda query: query.query == 'dog')
def query_photo(inline_query):
    results = set()
    while len(results) < 8:
        url = requests.get('https://api.thedogapi.com/v1/images/search').json()[0]['url']
        results.add(telebot.types.InlineQueryResultPhoto(f'cat{len(results)}', url, url))
    bot.answer_inline_query(inline_query.id, results, cache_time=1)


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                'content-type' in cherrypy.request.headers and \
                cherrypy.request.headers['content-type'] == 'application/json':

            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


def main():
    WEBHOOK_HOST = config.host
    WEBHOOK_PORT = config.port
    WEBHOOK_LISTEN = '0.0.0.0'

    WEBHOOK_SSL_CERT = './webhook_cert.pem'
    WEBHOOK_SSL_PRIV = './webhook_pkey.pem'

    WEBHOOK_URL_BASE = f'https://{WEBHOOK_HOST}:{WEBHOOK_PORT}'
    WEBHOOK_URL_PATH = f'/{config.token}/'

    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                    certificate=open(WEBHOOK_SSL_CERT, 'r'))

    access_log = cherrypy.log.access_log
    for handler in tuple(access_log.handlers):
        access_log.removeHandler(handler)

    cherrypy.config.update({
        'server.socket_host': WEBHOOK_LISTEN,
        'server.socket_port': WEBHOOK_PORT,
        'server.ssl_module': 'builtin',
        'server.ssl_certificate': WEBHOOK_SSL_CERT,
        'server.ssl_private_key': WEBHOOK_SSL_PRIV
    })

    cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})


if __name__ == '__main__':
    bot.remove_webhook()
    bot.polling(none_stop=True)
