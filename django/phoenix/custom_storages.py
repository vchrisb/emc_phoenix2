# # custom_storages.py
from django.conf import settings
from storages.backends.s3boto import S3BotoStorage

class StaticStorage(S3BotoStorage):
    bucket_name = settings.STATIC_BUCKET_NAME
    custom_domain = settings.STATIC_CUSTOM_DOMAIN
    # querystring_auth = True
    # secure_urls = True
    # querystring_expire = 30000

class MediaStorage(S3BotoStorage):
    bucket_name = settings.MEDIA_BUCKET_NAME
    custom_domain = settings.MEDIA_CUSTOM_DOMAIN
    # querystring_auth = True
    # secure_urls = True
    # querystring_expire = 30000

class SecureStorage(S3BotoStorage):
    bucket_name = settings.SECURE_BUCKET_NAME
    querystring_auth = True
    secure_urls = True
    querystring_expire = 300
    default_acl = "private"
