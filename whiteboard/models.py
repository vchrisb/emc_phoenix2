from django.db import models
from django.utils import timezone
from django.core.files.base import ContentFile

import uuid
import io, os

from django_resized import ResizedImageField
from django.conf import settings
from django.core.files.storage import get_storage_class

def WhiteboardImageName(instance, filename):
    extension = filename.split('.')[-1]
    return '{}/{}.{}'.format('WhiteboardImages', str(uuid.uuid4()), extension)

class Whiteboard(models.Model):
    """( description)"""
    SecureStorage = get_storage_class(settings.SECURE_FILE_STORAGE)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, blank=True, null=True)
    account = models.CharField(max_length=40)
    text = models.TextField(max_length=320)
    date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to=WhiteboardImageName, storage=SecureStorage())
    img_large = ResizedImageField(blank = True, size=[1024, 1024], upload_to='WhiteboardImages/thumb', storage=SecureStorage())
    img_medium = ResizedImageField(blank = True, size=[600, 800], upload_to='WhiteboardImages/thumb', storage=SecureStorage())
    img_small = ResizedImageField(blank = True, size=[340, 340], upload_to='WhiteboardImages/thumb', storage=SecureStorage())
    img_thumb = ResizedImageField(blank = True, size=[150, 150], crop=['middle', 'center'], upload_to='WhiteboardImages/thumb', storage=SecureStorage())

    __original_image = None

    def __str__(self):
        return str(self.user)

    def __init__(self, *args, **kwargs):
        super(Whiteboard, self).__init__(*args, **kwargs)
        self.__original_image = str(self.image)

    def save(self, *args, **kwargs):
        super(Whiteboard, self).save(*args, **kwargs)
        if str(self.image) != self.__original_image:
            image_source = self.image.file.read()
            image_content = ContentFile(image_source)
            image_name = os.path.split(self.image.file.name)[-1]
            image_name, image_ext = os.path.splitext(image_name)
            self.img_large.save(image_name + '_large' + image_ext, image_content, save=False)
            self.img_medium.save(image_name + '_medium' + image_ext, image_content, save=False)
            self.img_small.save(image_name + '_small' + image_ext, image_content, save=False)
            self.img_thumb.save(image_name + '_thumb' + image_ext, image_content, save=False)
        super(Whiteboard, self).save(*args, **kwargs)
        self.__original_image = str(self.image)
