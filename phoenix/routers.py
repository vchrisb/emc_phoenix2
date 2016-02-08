from rest_framework import routers

from .viewsets import UserViewSet, GroupViewSet
from mytwitter.viewsets import TweetViewSet, TweetPicViewSet
from vault.viewsets import DocumentGroupViewSet, DocumentViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'group', GroupViewSet)
router.register(r'tweet', TweetViewSet)
router.register(r'tweetpic', TweetPicViewSet)
router.register(r'documentgroup', DocumentGroupViewSet)
router.register(r'document', DocumentViewSet)
