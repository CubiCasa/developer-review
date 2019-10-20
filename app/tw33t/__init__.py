from flask import Flask
import sys
import os
from config import DevConfig, ProductionConfig
import logging
from twitter import Twitter, OAuth

app = Flask(__name__)
application = app

from tw33t.views import main


def init_logging(app_config):
    logging_config = dict()
    logging_config['format'] = '%(asctime)s - %(message)s'
    logging_config['datefmt'] = '%y-%m-%d %H:%M:%S'
    logging_config['level'] = logging.DEBUG if app_config['DEBUG'] else logging.INFO
    logging.basicConfig(**logging_config)
    logger = logging.getLogger("Tw33tLogger")
    log_folder = app.root_path + '/logs/'
    os.makedirs(log_folder, exist_ok=True)
    log_path = log_folder + app_config['LOGGING_FILENAME']
    logger.addHandler(logging.FileHandler(log_path))

    return logger


def init_twitter_client(app_config):
    auth = OAuth(app_config['TWITTER_TOKEN'],
                 app_config['TWITTER_TOKEN_SECRET'],
                 app_config['TWITTER_CONSUMER_KEY'],
                 app_config['TWITTER_CONSUMER_SECRET'])

    return Twitter(domain='api.twitter.com',
                   auth=auth)


env = os.environ.get('APP_ENV', 'Dev')
if env == 'prod':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevConfig)

# init logging
app.twitter_logger = init_logging(app.config)

# init twitter client
app.twitter_client = init_twitter_client(app.config)

# Register main page
app.register_blueprint(main.main_page)

# Register api
app.register_blueprint(main.backend_api, url_prefix='/api/v1')
