from django.db import models
from django.utils import timezone
import datetime
from phoenix.custom_storages import SecureStorage

# Create your models here.
class Entry(models.Model):
    """( description)"""
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    speaker = models.CharField(max_length=100, blank=True, default='')
    location = models.CharField(max_length=100)
    publish = models.BooleanField(default=False)
    hospitality = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

    def get_duration(self):
        timedelta = self.end - self.start
        timedelta = int(timedelta.seconds / 60)
        return timedelta

    def is_happening(self):
            """Return True if the event is happening 'now', False if not."""
            now = timezone.now()
            start = self.start
            end = self.end
            happening = False
            # check that the event has started and 'now' is btwn start & end:
            if (now >= start) and (start.time() <= now.time() <= end.time()):
                happening = True
            return happening
