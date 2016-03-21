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

"""
def AvatarName(instance, filename):
    extension = filename.split('.')[-1]
    return '{}/{}.{}'.format('Profile/avatar', str(uuid.uuid4()), extension)

class Profile(models.Model):
    SecureStorage = get_storage_class(settings.SECURE_FILE_STORAGE)
    emc_offices = (
        ('schwalbach', 'EMC Schwalbach'),
        ('public', 'Public'),
        ('private', 'Private'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('auth.User')
    description = models.TextField(max_length=320)
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100, choices=emc_offices)
    update = models.DateTimeField(default=timezone.now) # aktualisiert
    avatar = ResizedImageField(size=[150, 150], crop=['middle', 'center'], upload_to=AvatarName, storage=SecureStorage())

class SME(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey('Profile')
    expert_in_topic = #liste
    expert_in_vertical = #liste
    level_adressable = #liste

class SocialAccounts(models.Model):
    social = (
        ('twitter', 'Twitter'),
        ('xing', 'Xing'),
        ('github', 'GitHub'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey('Profile')
    account_type = models.CharField(max_length=100, choices=social)
    account_uid =
"""
