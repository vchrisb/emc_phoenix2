from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import json
import logging
import sys
import socket
import time
import tweepy

from mytwitter.tasks import print_url,save_tweet

logger = logging.getLogger('Stream_Logger')
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')

# Create a handler to write low-priority messages to a file.
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

#self.stdout.write("Unterminated line", ending='')

class Command(BaseCommand):
    help = 'Starts the twitter watcher'

    def add_arguments(self, parser):
        parser.add_argument('--keywords',dest='keywords', nargs='+', type=str, required=True)

    def handle(self, *args, **options):
        auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
        error_handler = ErrorHandler()
        while True:
            try:
                logger.info('Started')
                logger.debug(options['keywords'])
                stream = tweepy.Stream(auth, Listener(), timeout=None)
                stream.filter(track=options['keywords'])
            except Exception as e:
                if error_handler.error_count > 10:
                    logger.critical('Exceeded 10 errors. Aborted.')
                    break
                if isinstance(e, tweepy.error.TweepError) and (e.args[0] == 420 or e.args[0] >= 500):
                    error_handler.rate_limit(e.args[0])
                elif isinstance(e, tweepy.error.TweepError):
                    error_handler.http_error(e.args[0])
                elif isinstance(e, socket.error):
                    error_handler.network_error()
                else:
                    raise e

        logger.info('Finished.')
        logging.shutdown()

class Listener(tweepy.StreamListener):

    def on_data(self, tweet):

        tweet = json.loads(tweet)
        # if more than 1% of firehorse is addressed by filter, a limit message is sent with number of missed tweets
        if 'limit' in tweet:
            logger.warning("Missed tweets: " + str(tweet['limit']['track']))
            return
        if 'retweeted_status' in tweet:
            logger.debug('skipping - tweet is a retweet')
            return
        if 'possibly_sensitive' in tweet:
            if tweet['possibly_sensitive']:
                logger.debug('skipping - tweet is possibly sensitive')
                return
        save_tweet.delay(tweet)
        logger.debug('new tweet')

    def on_error(self, status_code):
        """Raise errors that occur."""
        raise tweepy.error.TweepError(status_code)

class ErrorHandler(object):
    """Handles errors raised by the Twitter Streaming API.

    This class contains methods to handle various types of errors that
    may occur while connecting to the Streaming API. Each method
    sleeps, logs the error, and increments the error count. The sleep
    durations and error count are reset if the last error occurred more
    than 60 minutes ago.

    See also: https://dev.twitter.com/docs/streaming-apis/connecting

    Attributes:
    sleep_{rate_limit, http_error, network_error, db_error}:
    Seconds to sleep before retrying the API connection.
    error_count: Number of errors that have occurred.
    time_of_last_error: The Unix time when the last error occurred.
    """

    def __init__(self):
        """Initializes class with default parameter values."""
        self._reset()

    def _reset(self):
        """Reset class parameters to default values."""
        self.sleep_rate_limit = 60
        self.sleep_http_error = 5
        self.sleep_network_error = .25
        self.error_count = 0
        self.time_of_last_error = time.time()

    def _decorator(func):
        """Reset (if necessary) and increment class parameters."""
        def wrapper(self, *args):
            if time.time() - self.time_of_last_error > 60 * 60:
                self._reset() # No errors occured in the past 60 minutes.
            func(self, *args)
            self.error_count += 1
            self.time_of_last_error = time.time()
        return wrapper

    @_decorator
    def rate_limit(self, status_code):
        msg = 'HTTP error, status code {}. Retrying in {} seconds.'
        msg = msg.format(status_code, self.sleep_rate_limit)
        logger.error(msg)
        time.sleep(self.sleep_rate_limit)
        self.sleep_rate_limit *= 2

    @_decorator
    def http_error(self, status_code):
        msg = 'HTTP error, status code {}. Retrying in {} seconds.'
        msg = msg.format(status_code, self.sleep_http_error)
        logger.error(msg)
        time.sleep(self.sleep_http_error)
        self.sleep_http_error = min(self.sleep_http_error * 2, 320)

    @_decorator
    def network_error(self):
        msg = 'TCP/IP error. Retrying in {} seconds.'
        msg = msg.format(self.sleep_network_error)
        logger.error(msg)
        time.sleep(self.sleep_network_error)
        self.sleep_network_error = min(self.sleep_network_error + 1, 16)
