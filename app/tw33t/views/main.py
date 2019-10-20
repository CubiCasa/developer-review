from flask import g, Markup
from flask import (Blueprint, render_template, make_response, redirect, url_for, abort, request, Response)
from tw33t import app
from jinja2 import TemplateNotFound
from functools import wraps
from flask import jsonify
from twitter import *
import json, requests, datetime, sys, os, uuid, re, time

main_page = Blueprint('main_page', __name__, template_folder='../templates')


@main_page.route('/', methods=['GET'])
def index():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)


'''

Introduce a "Get tweets" route for the client and log relevant info from each search into a file.

'''

backend_api = Blueprint('backend_api', __name__)


@backend_api.route('/getTweets', methods=['GET'])
def get_tweets():
    twitter_user = request.args.get('user')
    tweet_count = request.args.get('count', 10)
    logger = app.twitter_logger
    try:
        logger.info("User @{} : Start searching ...".format(twitter_user))
        tweets = app.twitter_client.statuses.user_timeline(screen_name=twitter_user,
                                                           count=tweet_count)
        for tweet in tweets:
            logger.info("User @{} : found tweet {}".format(twitter_user, tweet['text']))
        return jsonify(tweets)

    except TwitterHTTPError as twitter_error:
        if twitter_error.e.code == 404:
            logger.warning("User @{} : Not Found".format(twitter_user))
        elif twitter_error.e.code == 401:
            logger.warning("User @{} : No Permission".format(twitter_user))
        else:
            logger.error("User @{} : Twitter API Error [{}]".format(twitter_user, str(twitter_error)))

        abort(twitter_error.e.code)

    except Exception as other_error:
        logger.error("User @{} : Internal Server Error [{}]".format(twitter_user, str(other_error)))
        abort(500)
