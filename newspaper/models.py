import datetime
from django.db import models


class Newspaper(models.Model):
    name = models.CharField(max_length=32)
    url = models.URLField(max_length=128)
    morning = models.TimeField(default=datetime.time(10, 0))
    afternoon = models.TimeField(default=datetime.time(16, 0))
    night = models.TimeField(default=datetime.time(22, 0))
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
