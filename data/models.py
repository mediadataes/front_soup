from django.db import models
from django.conf import settings

from newspaper.models import Newspaper


class Data(models.Model):
    newspaper = models.ForeignKey(Newspaper, on_delete=models.CASCADE)
    html = models.TextField()
    created = models.DateTimeField(auto_now=True)

    def get_text_parts_that_contain(self, text, icase=True, amount_letters=40):
        text_parts = []
        if len(text) >= 3:
            content = self.html.lower() if icase else self.html[:]
            text = text.lower() if icase else text
            search = content.find(text)
            while search != -1:
                ini = search - amount_letters
                end = search + len(text) + amount_letters
                text_parts.append(self.html[ini:end].replace('\n', ''))
                search = content.find(text, search + 1)
        return text_parts

    def __str__(self):
        return '{} - {}'.format(self.newspaper.name,
                                self.created.strftime(settings.DT_FORMAT))
