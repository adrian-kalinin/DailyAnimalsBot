token = ''
admins = (0, )

host = ''
port = 8443
listen = '0.0.0.0'

webhook_url = f'https://{host}:{port}/{token}'

key_path = 'pkey.pem'
cert_path = 'cert.pem'
database_path = 'users'

api_base_url = 'https://api.the{}api.com/v1/images/search?mime_type=jpg'
max_inline_pics = 8
max_attempts = 3
