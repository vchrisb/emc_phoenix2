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
        parser.add_argument('--limit',dest='limit', type=int, required=False, default=10000)

    def handle(self, *args, **options):
        auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)

        if options['query']:
            for tweet in tweepy.Cursor(api.search,q=options['query'], rpp=100, result_type="recent", include_entities=True, lang="en").items(options['limit']):
               tweet = json.loads(json.dumps(tweet._json))
               if 'retweeted_status' in tweet:
                   print('%s skipping - tweet is a retweet' %(tweet['id']))
                   continue
               if 'possibly_sensitive' in tweet:
                   if tweet['possibly_sensitive']:
                       print('%s skipping - tweet is possibly sensitive' %(tweet['id']))
                       continue
               save_tweet.delay(tweet)
               print('%s processed - send tweet to queue' %(tweet['id']))

        if options['id']:
            for tweet in api.statuses_lookup(options['id'], include_entities=True):
               tweet = json.loads(json.dumps(tweet._json))
               save_tweet.delay(tweet)
