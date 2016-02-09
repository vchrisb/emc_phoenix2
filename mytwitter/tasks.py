from __future__ import absolute_import

from celery import shared_task
from .models import Tweet, TweetPic
import uuid
import pytz
from django.utils import timezone
from django.core.files.base import ContentFile
from django.db import transaction
from tweepy.utils import parse_datetime

@shared_task
def print_url(tweet):
    print(tweet['text'])

@shared_task
@transaction.atomic
def save_tweet(tweetobj):
    twitter_id = tweetobj['id']
    username = tweetobj['user']['name']
    screenname = tweetobj['user']['screen_name']
    text = tweetobj['text']
    created_at = parse_datetime(tweetobj['created_at'])
    created_at = timezone.make_aware(created_at, timezone=pytz.UTC) #tweets are stored int UTC

    image_urls = []
    try:
        for media in tweetobj['entities']['media']:
            if media['type'] == 'photo':
                image_urls.append(media['media_url'] + ":large")
                # cut image url  from tweet text
                text = text.replace(media['url'],"")
    except KeyError:
        pass
        # print("no picture")
        # return  # no picture

    # if len(image_urls) < 2:
    #     print ("less than 2 pictures" + str(len(image_urls)))
    #     return
    # create tweet
    newtweet, created  = Tweet.objects.get_or_create(twitter_id=twitter_id, username=username, screenname=screenname, text=text, created_at=created_at, from_twitter=True)
    if created:
        if image_urls:
            for image_url in image_urls:
                image = retrieve_image(image_url)
                image = process_image(image) # returns jpg
                image_name = "tmp.jpg" # will be renamed by model save function
                newpic = TweetPic()
                newpic.tweet = newtweet
                newpic.picture.save(image_name,image,save=False)
                newpic.save()
        print("saved tweet with id %s" %(str(twitter_id)))
    else:
        print(" tweet with id %s already exists" %(str(twitter_id)))

import urllib.request
from PIL import ImageFilter, Image
def retrieve_image(image_url):
    """
    Retrieves the image from the web
    """
    im = None
    try:
        im = Image.open(urllib.request.urlopen(image_url))  #Try to get the image, but if it fails
    except IOError as e:
        return None
    return im

import io
def process_image(image):
    maxsize = (1024, 1024)
    image.thumbnail(maxsize)
    image_io = io.BytesIO()
    image.save(image_io, 'jpeg')  #store it as a JPG
    image = ContentFile(image_io.getvalue())
    return image  #and give back the image
