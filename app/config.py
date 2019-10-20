import os
from twitter.cmdline import CONSUMER_KEY, CONSUMER_SECRET


class Config(object):
    DEBUG = True

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True

    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_SESSION_KEY = os.environ.get('CSRF_SESSION_KEY', 'pleasechangeit')

    # Secret key for signing cookies
    SECRET_KEY = os.environ.get('SECRET_KEY', 'pleasechangeit')

    # Twitter API
    TWITTER_TOKEN = os.environ.get('TWITTER_TOKEN')
    TWITTER_TOKEN_SECRET = os.environ.get('TWITTER_TOKEN_SECRET')
    TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY', CONSUMER_KEY)
    TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET', CONSUMER_SECRET)

    LOGGING_FILENAME = os.environ.get('LOGGING_FILENAME', 'tw33t.log')


class DevConfig(Config):
    DEBUG = True
    # Some other configuration for development


class ProductionConfig(Config):
    # DEBUG has to be to False in a production environment for security reasons
    DEBUG = False
    # Some other configuration for production
