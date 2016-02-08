from rest_framework import viewsets

from .serializers import TweetSerializer, TweetPicSerializer
from .models import Tweet, TweetPic

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all().order_by('-created_at')
    serializer_class = TweetSerializer

class TweetPicViewSet(viewsets.ModelViewSet):
    queryset = TweetPic.objects.all()
    serializer_class = TweetPicSerializer
