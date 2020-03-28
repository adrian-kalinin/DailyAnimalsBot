from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, PhotoSize
from telegram.ext import CallbackContext
from telegram.error import TelegramError, NetworkError

from .database import DataBase

from functools import wraps
import logging
import time
import sys
import os


def send_action(action):
    def decorator(func):
        @wraps(func)
        def command_func(update: Update, context: CallbackContext, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context, *args, **kwargs)
        return command_func
    return decorator


def strip(string):
    return string.strip()


def stop_and_restart():
    from main import updater
    updater.stop()
    logging.info('Bot has been stopped.')
    os.execl(sys.executable, sys.executable, *sys.argv)


def send_mailing(bot, data: dict):
    successful, failed = 0, 0
    markup = None

    if data['button']:
        text, url = map(strip, data['button'].split('-'))
        button = InlineKeyboardButton(text, url=url)
        markup = InlineKeyboardMarkup([[button]])

    with DataBase() as db:

        for user_id in db.get_users():
            try:
                if data['photo']:
                    bot.send_photo(
                        chat_id=user_id, photo=PhotoSize(*data['photo']),
                        caption=data['text'], reply_markup=markup,
                        parse_mode='HTML'
                    )

                elif data['text']:
                    bot.send_message(
                        chat_id=user_id, text=data['text'],
                        reply_markup=markup, parse_mode='HTML'
                    )

                else:
                    return False

                successful += 1
                time.sleep(1 / 20)

            except NetworkError as ex:  # TODO: understand what the fuck is happening here
                print(f'{user_id} - fail:\n{ex}')
                # return 0, 0

            except TelegramError:
                db.del_user(user_id=user_id)
                failed += 1

        return successful, failed
