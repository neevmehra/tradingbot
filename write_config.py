# python 3.x
from configparser import ConfigParser

config = ConfigParser()

config.add_section('main')
config.set('main', 'CLIENT_ID', 'CLIENT_ID')
config.set('main', 'REDIRECT_URI', 'REDIRECT_URL')
config.set('main', 'JSON_PATH', 'PATH')
config.set('main', 'ACCOUNT_NUMBER', 'ACCT')

with open(file='config/config.ini', mode='w') as f:
    config.write(f)

