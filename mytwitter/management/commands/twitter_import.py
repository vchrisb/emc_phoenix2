from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import json
import tweepy

from mytwitter.tasks import save_tweet


class Command(BaseCommand):
    help = 'Import Tweets'

    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--query', dest='query', type=str)
        group.add_argument('--id', dest='id', nargs='*', type=str)

    def handle(self, *args, **options):
        auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)

        if options['query']:
            for tweet in tweepy.Cursor(api.search,q=options['query'], rpp=100, result_type="recent", include_entities=True, lang="en").items():
               tweet = json.loads(json.dumps(tweet._json))
               save_tweet.delay(tweet)

        if options['id']:
            for tweet in api.statuses_lookup(options['id'], include_entities=True):
               tweet = json.loads(json.dumps(tweet._json))
               save_tweet.delay(tweet)
