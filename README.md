# DailyAnimalsBot
Telegram bot that sends random cute pictures with cats and doggos.

# User Usage

Everything is pretty simple – just press a button and then get a picture; or you are able to user commands /cat and /dog if the telegram keyboard is unavailable.

![Example](https://github.com/adreex/DailyAnimalsBot/blob/master/pictures_for_readme/animals.jpg)

Do not forget to use inline mode. It provides you a possibility to send a cat or a dog in any chat. Type the username of the bot and choose one of the pictures.

![Example](https://github.com/adreex/DailyAnimalsBot/blob/master/pictures_for_readme/inline.jpg)

# Admin Usage

There are some features for admins of the bot. Firt off all, you should enter /admin command. Then you can check statistics and restart the bot. One more great feature is the possibility to send a message to all users.

![Example](https://github.com/adreex/DailyAnimalsBot/blob/master/pictures_for_readme/admin.jpg)

# Deployment

### Configurate `config.py`:

Create a Telegram Bot at t.me/BotFather and get the token of your bot, then put it as `token` variable.
Then you can enter for `admins` some ids of users who can use admins' commands.
Fill your `host` (server's ip) and `port` (443, 80, 88 or 8443).

### Generate quick'n'dirty SSL certificate (in terminal):

`openssl genrsa -out webhook_pkey.pem 2048`

`openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem`

Attention! When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply with the same value as your server's ip addres

### Create virtual environment for Python and install all requiremetns (in terminal):

`virtualenv venv --python=python3`

`source venv/bin/activate`

`pip install -r requiremetns.txt`

Just enter python main.py in your terminal.
