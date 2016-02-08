from django.db import models
from django.conf import settings
from django.core.files.storage import get_storage_class
import uuid

# Create your models here.
def DocumentFilename(instance, filename):
    filename = "documents/%s/%s" %(instance.documentgroup.id, filename)
    return (filename)

class DocumentGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)

class Document(models.Model):
    SecureStorage = get_storage_class(settings.SECURE_FILE_STORAGE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    documentgroup = models.ForeignKey(DocumentGroup, related_name='document')
    filename = models.FileField(upload_to=DocumentFilename, storage=SecureStorage())
    downloads = models.IntegerField(blank=True, default=0)
