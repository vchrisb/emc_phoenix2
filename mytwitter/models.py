from django.db import models
from django.utils import timezone
from django.core.files.base import ContentFile

import uuid
import io, os

from django_resized import ResizedImageField
from django.conf import settings
from django.core.files.storage import get_storage_class

# Create your models here.
class Tweet(models.Model):
    """( description)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    twitter_id = models.BigIntegerField(unique=True, blank=True, null=True)
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, blank=True, null=True)
    text = models.TextField(max_length=160)
    created_at = models.DateTimeField(default=timezone.now)
    username = models.CharField(max_length=20, blank=True)
    screenname = models.CharField(max_length=15, blank=True)
    from_twitter = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

def TweetPictureName(instance, filename):
    extension = filename.split('.')[-1]
    return '{}/{}.{}'.format('TweetPictures', str(uuid.uuid4()), extension)

class TweetPic(models.Model):
    SecureStorage = get_storage_class(settings.SECURE_FILE_STORAGE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tweet = models.ForeignKey(Tweet, related_name='pics')
    picture = models.ImageField(upload_to=TweetPictureName, storage=SecureStorage())
    pic_large = ResizedImageField(blank = True, size=[1024, 1024], upload_to='TweetPictures/thumb', storage=SecureStorage())
    pic_medium = ResizedImageField(blank = True, size=[600, 800], upload_to='TweetPictures/thumb', storage=SecureStorage())
    pic_small = ResizedImageField(blank = True, size=[340, 340], upload_to='TweetPictures/thumb', storage=SecureStorage())
    pic_thumb = ResizedImageField(blank = True, size=[150, 150], crop=['middle', 'center'], upload_to='TweetPictures/thumb', storage=SecureStorage())

    __original_picture = None

    def __init__(self, *args, **kwargs):
        super(TweetPic, self).__init__(*args, **kwargs)
        self.__original_picture = str(self.picture)

    def __str__(self):
        return str(self.picture.name)

    def save(self, *args, **kwargs):
        super(TweetPic, self).save(*args, **kwargs)
        if str(self.picture) != self.__original_picture:
            picture_source = self.picture.file.read()
            picture_content = ContentFile(picture_source)
            picture_name = os.path.split(self.picture.file.name)[-1]
            picture_name, picture_ext = os.path.splitext(picture_name)
            self.pic_large.save(picture_name + '_large' + picture_ext, picture_content, save=False)
            self.pic_medium.save(picture_name + '_medium' + picture_ext, picture_content, save=False)
            self.pic_small.save(picture_name + '_small' + picture_ext, picture_content, save=False)
            self.pic_thumb.save(picture_name + '_thumb' + picture_ext, picture_content, save=False)
        super(TweetPic, self).save(*args, **kwargs)
        self.__original_picture = str(self.picture)
