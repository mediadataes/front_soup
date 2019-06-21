import os
import requests
from celery import shared_task
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone

from newspaper.models import Newspaper
from .models import Data


@shared_task
def download_url(pk, strtime, url):
    newspaper = get_object_or_404(Newspaper, pk=pk)
    now = timezone.now().strftime('%d-%m-%Y')
    path = '{}/{}/{}'.format(now, newspaper.name, strtime).replace(' ', '_')
    save_dir = os.path.join(settings.STATIC_ROOT, path)
    command = 'wget -nd -E -k -H -p -P {} -A jpg,svg,gif,png,html,woff,css,js --restrict-file-names=windows -e robots=off {}'
    command = command.format(save_dir, url)
    os.popen(command)
    page = requests.get(url)
    content = page.text
    data = Data(newspaper=newspaper, path=path, html=content)
    data.save()
    return data.pk
