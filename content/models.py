from django.db import models
from django.conf import settings
from django.core.files.storage import get_storage_class
from django_resized import ResizedImageField

# Create your models here.
class Featurette(models.Model):
    """( description)"""
    privacy_choices = (
        ('public_only', 'Public only'),
        ('public', 'Public'),
        ('private', 'Private'),
    )
    SecureStorage = get_storage_class(settings.SECURE_FILE_STORAGE)
    
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    heading = models.CharField(max_length=100)
    content = models.TextField()
    image = ResizedImageField(size=[400, 400], crop=['middle', 'center'], upload_to='FeaturettePictures', storage=SecureStorage())
    position = models.IntegerField()
    publish = models.BooleanField(default=False)
    privacy = models.CharField(max_length=100, choices=privacy_choices, default='private')

class FAQ(models.Model):
    """( description)"""
    privacy_choices = (
        ('public_only', 'Public only'),
        ('public', 'Public'),
        ('private', 'Private'),
    )

    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    question = models.CharField(max_length=150)
    answer = models.TextField(max_length=500)
    position = models.IntegerField()
    publish = models.BooleanField(default=False)
    privacy = models.CharField(max_length=100, choices=privacy_choices, default='private')
