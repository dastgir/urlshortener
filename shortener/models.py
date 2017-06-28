from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
class Link(models.Model):
    id = models.IntegerField(primary_key=True)
    long_link = models.CharField(max_length=200)
    short_link = models.CharField(max_length=50)
    ip = models.GenericIPAddressField()
    date_added = models.DateTimeField('date created', auto_now_add=True)

    def __str__(self):
        return self.short_link

    def was_added_recently(self):
        return self.date_added >= timezone.now() - datetime.timedelta(days=1)

    @classmethod
    def create(cls, link, slink, ip):
        for short in slink:
            l = cls(long_link=link, short_link=short, ip=ip)
            l.save()
        return
