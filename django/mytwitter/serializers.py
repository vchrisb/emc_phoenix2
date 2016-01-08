from rest_framework import serializers
from .models import Tweet, TweetPic

class TweetPicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TweetPic
        fields = ('url', 'picture', 'pic_large', 'pic_medium', 'pic_small', 'pic_thumb' )

class TweetSerializer(serializers.HyperlinkedModelSerializer):
    pics = TweetPicSerializer(many=True, read_only=True)
    class Meta:
        model = Tweet
        fields = ('url', 'created_at', 'text', 'user', 'username', 'screenname', 'twitter_id', 'pics', 'from_twitter')
