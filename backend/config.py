import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

class BetfairConfig(object):
    USERNAME = os.environ.get('BETFAIR_USERNAME') or None
    PASSWORD = os.environ.get('BETFAIR_PASSWORD') or None
    APP_KEY = os.environ.get('BETFAIR_APP_KEY') or None
    CERT_FILE = os.environ.get('BETFAIR_CERT_FILE') or None
    CERT_KEY_FILE = os.environ.get('BETFAIR_CERT_KEY_FILE') or None
