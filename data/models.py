from django.db import models
from django.conf import settings

from newspaper.models import Newspaper


class Data(models.Model):
    newspaper = models.ForeignKey(Newspaper, on_delete=models.CASCADE)
    html = models.TextField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.newspaper.name,
                                self.created.strftime(settings.DT_FORMAT))
